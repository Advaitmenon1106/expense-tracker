import pypdfium2 as pdfium

PDF_PATH = "/home/advait/expense-tracker/statement_unlocked.pdf"

text = "\n".join(
    p.get_textpage().get_text_range() 
    for p in pdfium.PdfDocument(PDF_PATH)
)

print(text)