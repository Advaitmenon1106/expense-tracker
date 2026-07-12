import pdfplumber
import numpy as np
from sklearn.cluster import AgglomerativeClustering
from collections import defaultdict

pdf_path = "/home/advait/Downloads/Statement_DEC2025_010182581.pdf"
password = "ADVA1106"

with pdfplumber.open(pdf_path, password="ADVA1106") as pdf:
    page = pdf.pages[0]
    words = page.extract_words()

x_centers = np.array([
    [(w["x0"] + w["x1"]) / 2] for w in words
])

model = AgglomerativeClustering(
    linkage="ward",
    n_clusters=None,
    distance_threshold=40
)

labels = model.fit_predict(x_centers)

for word, label in zip(words, labels):
    word["column"] = label


columns = defaultdict(list)

for w in words:
    columns[w["column"]].append(w["text"])

for word in words:
    print(
        f"text={word['text']:<20} "
        f"x0={word['x0']:.1f} "
        f"x1={word['x1']:.1f} "
        f"x_center={(word['x0']+word['x1'])/2:.1f} "
        f"col={word['column']}"
    )

cluster_positions = {}

for col, words_in_col in columns.items():
    xs = [(w["x0"] + w["x1"]) / 2 for w in words if w["column"] == col]
    cluster_positions[col] = np.mean(xs)

ordered_cols = sorted(cluster_positions, key=lambda c: cluster_positions[c])

print("Column order:", ordered_cols)

# for col in sorted(columns):
#     print(f"\nCOLUMN {col}")
#     print(columns[col])  # first few words