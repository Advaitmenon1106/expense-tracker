from pdf2image import convert_from_bytes
from PIL import Image
import io
import base64
from fastapi.datastructures import UploadFile
import pandas as pd
from backend.utils.llm_tools import send_image_to_mistral
import yaml
import asyncio
import json
from io import BytesIO
from PyPDF2 import PdfReader

class DocIngestor:
    def __init__(self, user_inputs:list[UploadFile], pdf_password=""):
        self.user_inputs = user_inputs
        self.llm = send_image_to_mistral
        self.pdf_password = pdf_password

        with open('backend/utils/prompts.yml', 'r') as f:
            prompts= yaml.safe_load(f)
            self.prompts = prompts['statement_ingestor']
        
        with open('backend/Statement_Ingestor/extraction_template.json', 'rb') as f:
            self.extraction_template = json.load(f)

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
                        # Try decrypting with an empty password
                        pdf_reader.decrypt("")
                    
                    # Write the decrypted PDF to a BytesIO object
                    from PyPDF2 import PdfWriter
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
                            'type': 'image',
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
                        'inputs': pd.read_excel(user_input.file.read())
                    }
                )
            
            self.inputs = all_inputs

    async def img_to_json(self):
        system_prompt = self.prompts['pixtral_prompt_system']
        images = self.inputs['images']
        llm = self.llm

        tasks = []
        mapping = []

        for image_group in images:
            human_prompt = self.prompts['pixtral_prompt_human'].format(json_extraction_template=self.extraction_template)
            tasks.append(llm(images=image_group['inputs'], system_prompt=system_prompt, human_prompt=human_prompt))
            mapping.append(image_group)

        results = await asyncio.gather(*tasks)
        
        for i, r in enumerate(results):
            try:
                # Try to parse directly first
                mapping[i]['results'] = json.loads(r)
            except json.JSONDecodeError:
                try:
                    # If that fails, try to extract JSON from markdown code fences
                    import re
                    json_match = re.search(r'```(?:json)?\s*(.*?)\s*```', r, re.DOTALL)
                    if json_match:
                        mapping[i]['results'] = json.loads(json_match.group(1))
                    else:
                        # If still no match, store the raw result
                        mapping[i]['results'] = r.strip('```').strip('json')
                except Exception as e:
                    print(f"Error parsing JSON for {mapping[i]['filename']}: {e}")
                    mapping[i]['results'] = r
    
        return mapping
    

# Open files and read their content into BytesIO objects
with open("/home/advait/Downloads/Statement_DEC2025_010182581.pdf", "rb") as f:
    pdf_bytes = f.read()
pdf_file = UploadFile(filename="test.pdf", file=BytesIO(pdf_bytes))

with open("/home/advait/Downloads/test_page", "rb") as f:
    image_bytes = f.read()
image_file = UploadFile(filename="test.jpg", file=BytesIO(image_bytes))

# Instantiate the DocIngestor with test files
doc_ingestor = DocIngestor(user_inputs=[pdf_file, image_file], pdf_password="ADVA1106")

# Route the inputs
doc_ingestor.route_input()

# Run the img_to_json method and print the results
async def test_doc_ingestor():
    results = await doc_ingestor.img_to_json()
    print(results)

asyncio.run(test_doc_ingestor())