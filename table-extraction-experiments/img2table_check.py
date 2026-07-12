# from marker.converters.pdf import PdfConverter
# from marker.models import create_model_dict
# from marker.config.parser import ConfigParser
# from marker.converters.table import TableConverter
# from marker.models import create_model_dict
# from marker.output import text_from_rendered
from img2table.document import PDF
from img2table.ocr import TesseractOCR

ocr = TesseractOCR(lang="eng")


pdf_path = "/home/advait/Downloads/Statement_DEC2025_010182581.pdf"

from pypdf import PdfReader, PdfWriter

reader = PdfReader(pdf_path)
reader.decrypt("ADVA1106")

writer = PdfWriter()

for page in reader.pages:
    writer.add_page(page)

with open("statement_unlocked.pdf", "wb") as f:
    writer.write(f)


print("Starting extraction")

# converter = TableConverter(
#     artifact_dict=create_model_dict(),
# )

# pdf = PDF("statement_unlocked.pdf", 
#           detect_rotation=False,
#           pdf_text_extraction=True)

# extracted_tables = pdf.extract_tables(ocr=ocr,
#                                       implicit_rows=True,
#                                       implicit_columns=True,
#                                       borderless_tables=True,
#                                       min_confidence=50)


# for page, tables in extracted_tables.items():
#     print(f"\n--- PAGE {page} ---")

#     for i, table in enumerate(tables):
#         print(f"\nTable {i}")
#         print("Title:", table.title)
#         print(table.df)