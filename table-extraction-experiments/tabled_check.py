from tabled.extract import extract_tables
from tabled.fileinput import load_pdfs_images
from tabled.inference.models import load_detection_models, load_recognition_models, load_layout_models
import pandas as pd

det_models, rec_models, layout_models = load_detection_models(), load_recognition_models(), load_layout_models()
images, highres_images, names, text_lines = load_pdfs_images("/home/advait/expense-tracker/statement_unlocked.pdf")

page_results = extract_tables(images, highres_images, text_lines, det_models, layout_models, rec_models)
# print(page_results[0])

first_page = page_results[0]

for page_idx, page in enumerate(page_results):
    for table_idx, table in enumerate(page.rows_cols):

        nrows = max(r.row_id for r in table.rows) + 1
        ncols = max(c.col_id for c in table.cols) + 1

        matrix = [["" for _ in range(ncols)] for _ in range(nrows)]

        for cell in table.cells:

            center_x = (cell.bbox[0] + cell.bbox[2]) / 2
            center_y = (cell.bbox[1] + cell.bbox[3]) / 2

            row_id = None
            col_id = None

            for row in table.rows:
                if row.bbox[1] <= center_y <= row.bbox[3]:
                    row_id = row.row_id
                    break

            for col in table.cols:
                if col.bbox[0] <= center_x <= col.bbox[2]:
                    col_id = col.col_id
                    break

            if row_id is not None and col_id is not None:
                matrix[row_id][col_id] = cell.text.strip()

        df = pd.DataFrame(matrix)

        print(f"\nTABLE {table_idx}")
        print(df)

        df.to_csv(f"tables/table_{table_idx}.csv", index=False)