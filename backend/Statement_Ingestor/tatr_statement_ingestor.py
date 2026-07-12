from transformers import AutoModelForObjectDetection, AutoImageProcessor
from PIL import Image
import torch
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pdf2image import convert_from_path
from dotenv import load_dotenv
import cv2
import numpy as np
import yaml
from fastapi.datastructures import UploadFile
import json
from pypdf import PdfReader, PdfWriter
import io
from pdf2image import convert_from_bytes
import pandas as pd
from backend.utils.llm_tools import send_image_to_mistral, send_image_to_ollama
import re

load_dotenv()

_det_processor = None
_det_model = None
_struct_processor = None
_struct_model = None

def ensure_models_loaded():
    global _det_processor, _det_model
    global _struct_processor, _struct_model

    if _det_model is None:
        _det_processor = AutoImageProcessor.from_pretrained(
            "microsoft/table-transformer-detection"
        )
        _det_model = AutoModelForObjectDetection.from_pretrained(
            "microsoft/table-transformer-detection"
        )
        _det_model.eval()

    if _struct_model is None:
        _struct_processor = AutoImageProcessor.from_pretrained(
            "microsoft/table-transformer-structure-recognition"
        )
        _struct_model = AutoModelForObjectDetection.from_pretrained(
            "microsoft/table-transformer-structure-recognition"
        )
        _struct_model.eval()

    return (
        _det_processor,
        _det_model,
        _struct_processor,
        _struct_model,
    )



class DocIngestor:
    def __init__(self, user_inputs:list[UploadFile], pdf_password="", concurrency=1, imgs_per_call = 2):
        self.user_inputs = user_inputs
        self.pdf_password = pdf_password
        self.sem = asyncio.Semaphore(concurrency)
        self.imgs_per_call = imgs_per_call

        with open('/home/advait/expense-tracker/backend/Statement_Ingestor/prompts.yml', 'r') as f:
            prompts= yaml.safe_load(f)
            self.prompts = prompts
        
        with open('backend/Statement_Ingestor/extraction_template.json', 'rb') as f:
            self.extraction_template = json.load(f)

        self.det_processor, self.det_model, self.struct_processor, self.struct_model = ensure_models_loaded()

    def route_input(self):
        all_inputs = {
            'images': [],
            'sheets': [],
        }
        user_inputs = self.user_inputs

        for user_input in user_inputs:
            if user_input.filename.lower().endswith((".png", ".jpg", ".jpeg")):
                image_bytes = user_input.file.read()
                image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
                all_inputs['images'].append(
                    {
                        'filename':user_input.filename,
                        'type': 'image',
                        'inputs': [image]
                    }
                )

            elif user_input.filename.lower().endswith(".pdf"):
                user_input.file.seek(0)
                pdf_bytes = user_input.file.read()
                
                # Try to decrypt the PDF if it's password-protected
                try:
                    pdf_reader = PdfReader(io.BytesIO(pdf_bytes))
                    if pdf_reader.is_encrypted:
                        result = pdf_reader.decrypt(self.pdf_password)
                        if result == 0:
                            raise ValueError("Incorrect PDF password")
                    
                    # Write the decrypted PDF to a BytesIO object
                    pdf_writer = PdfWriter()
                    for page in pdf_reader.pages:
                        pdf_writer.add_page(page)
                    
                    decrypted_bytes = io.BytesIO()
                    pdf_writer.write(decrypted_bytes)
                    decrypted_bytes.seek(0)
                    images = convert_from_bytes(decrypted_bytes.read())

                    all_inputs['images'].append(
                        {
                            'filename': user_input.filename,
                            'type': 'PDF',
                            'inputs': images
                        }
                    )
                
                except Exception as e:
                    print(f"Error decrypting PDF {user_input.filename}: {e}")
                    continue
                
            
            elif user_input.filename.lower().endswith(('.xlsx', '.xls')):
                user_input.file.seek(0)
                all_inputs['sheets'].append(
                    {
                        'filename': user_input.filename,
                        'type': 'spreadsheet',
                        'inputs': pd.read_excel(user_input.file)
                    }
                )

        self.all_inputs = all_inputs

    

    async def classify(self, imgs):
        async with self.sem:
            response = await send_image_to_mistral(
                imgs,
                self.prompts["classify_cropped_table"]["system"],
                self.prompts["classify_cropped_table"]["human"],
            )

        if response.startswith("```"):
            response = re.search(
                r"```(?:json)?\s*(.*?)\s*```",
                response,
                re.DOTALL,
            ).group(1)

        return json.loads(response)


    async def table_extract(self):
        table_det_processor = self.det_processor
        table_det_model = self.det_model

        table_struct_processor = self.struct_processor
        table_struct_model = self.struct_model
        

        image_entries:list[dict] = self.all_inputs['images']

        table_det_outputs = []

        for document in image_entries:
            page_images = document["inputs"]

            inputs = table_det_processor(
                images=page_images,
                return_tensors="pt"
            )

            with torch.inference_mode():
                outputs = table_det_model(**inputs)
            
            target_sizes = torch.tensor([
                page.size[::-1]
                for page in page_images
            ])

            det_results = table_det_processor.post_process_object_detection(
                outputs,
                threshold=0.7,
                target_sizes=target_sizes
            )

            table_det_outputs.append(det_results)

        padding = 20

        for i, doc in enumerate(table_det_outputs):
            corresponding_statement_page_images:Image = image_entries[i]['inputs']

            image_entries[i]['detected_tables_images'] = []

            corresponding_table_detection_results = table_det_outputs[i]

            for j, img in enumerate(corresponding_statement_page_images):
                page_detection = corresponding_table_detection_results[j]

                if len(page_detection['boxes']) == 0:
                    continue

                multiple_tables = []
                for coords in page_detection["boxes"]:
                    x1, y1, x2, y2 = map(int, coords.tolist())
                    
                    x1 = max(0, x1 - padding)
                    y1 = max(0, y1 - padding)
                    x2 = min(img.width, x2 + padding)
                    y2 = min(img.height, y2 + padding)

                    table_img = img.crop((x1, y1, x2, y2))
                    multiple_tables.append(table_img)

                
                actual_tables = []

                tasks = []

                for idx in range(0, len(multiple_tables), self.imgs_per_call):
                    imgs = multiple_tables[idx:idx+self.imgs_per_call]

                    tasks.append(self.classify(imgs))

                batch_results = await asyncio.gather(*tasks)
                classfns = [
                    item
                    for batch in batch_results
                    for item in batch
                ]

                for k, cl in enumerate(classfns):
                    if cl["is_statement"].lower() == "true":
                        actual_tables.append(multiple_tables[k])

                image_entries[i]['detected_tables_images'].append(actual_tables)

            print(image_entries)

        
        # structure extraction from image_entries['detected_tables_images']: -

        


import asyncio
from fastapi.datastructures import UploadFile


async def main():
    pdf_path = "/home/advait/expense-tracker/statement_unlocked.pdf"

    with open(pdf_path, "rb") as f:
        upload_file = UploadFile(
            filename="statement.pdf",
            file=f
        )

        ingestor = DocIngestor(
            user_inputs=[upload_file],
            pdf_password=""
        )

        ingestor.route_input()

        await ingestor.table_extract()

        print("\n=== RESULTS ===\n")

        for doc in ingestor.all_inputs["images"]:
            print(f"Document: {doc['filename']}")

            detected_tables = doc.get("detected_tables_images", [])

            print(f"Pages with extracted tables: {len(detected_tables)}")

            for page_idx, page_tables in enumerate(detected_tables):
                print(
                    f"Page {page_idx + 1}: "
                    f"{len(page_tables)} selected tables"
                )

                for table_idx, table_img in enumerate(page_tables):
                    print(
                        f"  Table {table_idx + 1}: "
                        f"{table_img.size}"
                    )

                    # Optional: save crops to inspect
                    table_img.save(
                        f"debug_test/debug_page_{page_idx+1}_table_{table_idx+1}.png"
                    )


if __name__ == "__main__":
    asyncio.run(main())