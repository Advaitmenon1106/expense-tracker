import os

# Must be set BEFORE importing paddle/paddleocr/paddlex
# os.environ["FLAGS_enable_pir_api"] = "0"
# os.environ["FLAGS_use_mkldnn"] = "0"

from dotenv import load_dotenv
from paddleocr import PaddleOCR

load_dotenv()

from paddlex import create_pipeline
import numpy as np
from PIL import Image


table_crop = np.asarray(
    Image.open(
        "/home/advait/expense-tracker/debug_test/debug_page_13_table_1.png"
    )
)

pipeline = PaddleOCR(
    lang="en",
    ocr_version="PP-OCRv4",
    enable_mkldnn=False,  # prevents MKLDNN/PIR crash
)

output = pipeline.predict(
    input=table_crop,
)

for res in output:
    res.print()

    res.save_to_json("./output/")
    res.save_to_img("./output/")