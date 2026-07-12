from transformers import AutoModelForObjectDetection, AutoImageProcessor
from PIL import Image
import torch
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pdf2image import convert_from_path
from dotenv import load_dotenv
import cv2
import numpy as np

load_dotenv()

# --- Load both models ---
det_processor = AutoImageProcessor.from_pretrained("microsoft/table-transformer-detection")
det_model = AutoModelForObjectDetection.from_pretrained("microsoft/table-transformer-detection")
det_model.eval()

str_processor = AutoImageProcessor.from_pretrained("microsoft/table-transformer-structure-recognition")
str_model = AutoModelForObjectDetection.from_pretrained("microsoft/table-transformer-structure-recognition")
str_model.eval()

# --- Stage 1: detect table on full page ---
page = convert_from_path('/home/advait/expense-tracker/statement_unlocked.pdf')[0].convert("RGB")

inputs = det_processor(images=page, return_tensors="pt")
with torch.no_grad():
    outputs = det_model(**inputs)

target_sizes = torch.tensor([page.size[::-1]])
det_results = det_processor.post_process_object_detection(
    outputs, threshold=0.7, target_sizes=target_sizes
)[0]

x1, y1, x2, y2 = map(int, det_results['boxes'][0].tolist())

padding = 40

x1 = max(0, x1 - padding)
y1 = max(0, y1 - padding)
x2 = min(page.width, x2 + padding)
y2 = min(page.height, y2 + padding)

table = page.crop((x1, y1, x2, y2))

# table.save('idk.jpeg')
# print(det_results['boxes'][0])


inputs_table = str_processor(images=table, return_tensors="pt")
with torch.no_grad():
    outputs_str = str_model(**inputs_table)

target_sizes = torch.tensor([table.size[::-1]])
str_results = str_processor.post_process_object_detection(
    outputs_str, threshold=0.7, target_sizes=target_sizes
)[0]

# print(list(str_results.keys))
# boxes = outputs_str.pred_boxes

table = np.array(table)

for i, box in enumerate(str_results["boxes"]):
    label = str_results['labels'][i]

    label_name = str_model.config.id2label[label.item()]
    if label_name == "table row":
        x1, y1, x2, y2 = map(int, box.tolist())
        table = cv2.rectangle(table, (np.ceil(x1), np.ceil(y1)), (np.ceil(x2), np.ceil(y2)), (255, 0, 0), 2)

    if label_name == "table column header":
        x1, y1, x2, y2 = map(int, box.tolist())
        table = cv2.rectangle(table, (np.ceil(x1), np.ceil(y1)), (np.ceil(x2), np.ceil(y2)), (0, 255, 0), 2)


Image.fromarray(table).save('annotated.png')
Image.fromarray(table[y1:y2, x1:x2]).save('one_example.png')

print(list(str_results['labels']))

print(str_model.config.id2label)

for label, box in zip(
    str_results["labels"],
    str_results["boxes"]
):
    print(
        str_model.config.id2label[label.item()],
        box.tolist()
    )