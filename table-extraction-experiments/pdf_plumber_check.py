import pdfplumber

with pdfplumber.open("/home/advait/expense-tracker/statement_unlocked.pdf") as pdf:
    for p in pdf.pages:
        for t in p.extract_tables():
            print(t)