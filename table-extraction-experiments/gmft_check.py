# new in v0.3: gmft.auto
from gmft.auto import CroppedTable, TableDetector, AutoTableFormatter, AutoTableDetector
from gmft.pdf_bindings import PyPDFium2Document
import pandas as pd
from gmft.formatters.tatr import TATRFormatConfig, TATRTableFormatter
from gmft.auto import AutoTableFormatter

config = TATRFormatConfig()
# config.force_large_table_assumption = True  # or False
# config.formatter_base_threshold = 0.3
# config.cell_required_confidence = {
#     0: 0.3,  # table
#     1: 0.3,  # column
#     2: 0.3,  # row
#     3: 0.3,  # column header
#     4: 0.3,  # projected row header
#     5: 0.3,  # spanning cell
#     6: 99,   # no object — keep this high, it's the "nothing here" class
# }


PDF_PATH = "/home/advait/expense-tracker/statement_unlocked.pdf"

detector = AutoTableDetector()
formatter = AutoTableFormatter(config=config)

def ingest_pdf(pdf_path): # produces list[CroppedTable]
    doc = PyPDFium2Document(pdf_path)
    tables = []
    for page in doc:
        tables += detector.extract(page)
    return tables, doc

tables, doc = ingest_pdf(PDF_PATH)

print(len(tables))

# with pd.ExcelWriter("tables3.xlsx", engine="openpyxl") as writer:
# for i, t in enumerate(tables):
#     ft = formatter.extract(t)
#     df = ft.df(config_overrides={"enable_multi_header": True})
#     # if not df.empty:
#     #     df.to_excel(writer, sheet_name=f"Table_{i}", index=False)
#     print(df, end='\n\n\n')

with open("tables.md", "w") as f:
    for i, t in enumerate(tables):
        ft = formatter.extract(t)
        df = ft.df(config_overrides={"enable_multi_header": True})
        f.write(f"## Table {i}\n\n")
        f.write(df.to_markdown(index=False))
        f.write("\n\n")

doc.close()