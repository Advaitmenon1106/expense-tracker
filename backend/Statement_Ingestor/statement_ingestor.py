from mistralai import Mistral
from dotenv import load_dotenv
import os
from pdf2image import convert_from_bytes
from PIL import Image
import io
import base64
from fastapi.datastructures import UploadFile
import pandas as pd


class DocIngestor:
    def __init__(self, user_inputs:list[UploadFile]):
        self.user_inputs = user_inputs

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
                images = convert_from_bytes(pdf_bytes)

                all_inputs['images'].append(
                    {
                        'filename': user_input.filename,
                        'type': 'image',
                        'inputs': images
                    }
                )
            
            elif user_input.filename.lower().endswith(('.csv')):
                user_input.file.seek(0)
                all_inputs['sheets'].append(
                    {
                        'filename': user_input.filename,
                        'type': 'spreadsheet',
                        'inputs': pd.read_csv(user_input.file.read())
                    }
                )
            
            elif user_input.filename.lower().endswith(('.xlsx', '.xls')):
                user_input.file.seek(0)
                all_inputs['sheets'].append(
                    {
                        'filename': user_input.filename,
                        'type': 'spreadsheet',
                        'inputs': pd.read_excel(user_input.file.read())
                    }
                )
        
    async def handle_pdfs(self):
        pass