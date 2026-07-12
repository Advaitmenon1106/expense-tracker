import camelot

PDF_PATH = "/home/advait/expense-tracker/statement_unlocked.pdf"

# Read tables
a = camelot.read_pdf()

# Print first table
print(a)