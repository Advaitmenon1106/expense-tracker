import fitz 


PDF_PATH = "/home/advait/expense-tracker/statement_unlocked.pdf"


d = fitz.open(PDF_PATH)
for p in d:
    t = p.get_text("dict")
    print(t)