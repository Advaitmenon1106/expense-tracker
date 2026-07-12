import pdfplumber
import numpy as np
from sklearn.cluster import AgglomerativeClustering
from collections import defaultdict
from scipy.signal import find_peaks


pdf_path = "/home/advait/Downloads/Statement_DEC2025_010182581.pdf"
password = "ADVA1106"

with pdfplumber.open(pdf_path, password="ADVA1106") as pdf:
    page = pdf.pages[0]
    words = page.extract_words()

x_centers = np.array([
    [(w["x0"] + w["x1"]) / 2] for w in words
])


x_centers = np.array([(w["x0"] + w["x1"]) / 2 for w in words])
hist, bins = np.histogram(x_centers, bins=60)

peaks, _ = find_peaks(hist, prominence=5)
column_x = bins[peaks]

print("Detected column centers:", column_x)

columns = []

for w in words:
    x_center = (w["x0"] + w["x1"]) / 2
    col = np.argmin(np.abs(column_x - x_center))
    w["column"] = col



rows = defaultdict(list)

for w in words:
    y = round(w["top"]/5)*5
    rows[y].append(w)



table = []

for y in sorted(rows):
    row_words = rows[y]
    cells = defaultdict(list)

    for w in row_words:
        cells[w["column"]].append(w["text"])

    row = [" ".join(cells[c]) for c in range(len(column_x))]
    table.append(row)

for r in table:
    print(r)