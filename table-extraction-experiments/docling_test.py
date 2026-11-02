from docling.document_converter import DocumentConverter
from pathlib import Path
from PIL import Image
import pandas as pd

from dotenv import load_dotenv
load_dotenv()

converter = DocumentConverter()

# Pick one existing crop
image_path = '/home/advait/expense-tracker/debug_test/debug_page_13_table_1.png'

# Convert
result = converter.convert(str(image_path))

doc = result.document

# Inspect Markdown
markdown = doc.export_to_markdown()
print(markdown)

# Inspect structured tables
print(f"Tables detected: {len(doc.tables)}")

for i, table in enumerate(doc.tables):
    df = table.export_to_dataframe(doc=doc)
    print(f"\nTable {i + 1}")
    print(df)