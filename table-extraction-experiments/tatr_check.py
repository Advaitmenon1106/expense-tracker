import matplotlib.pyplot as plt
import matplotlib.patches as patches
from transformers import AutoModelForObjectDetection, AutoImageProcessor
from PIL import Image
import torch
from pdf2image import convert_from_path

processor = AutoImageProcessor.from_pretrained("microsoft/table-transformer-detection")
model = AutoModelForObjectDetection.from_pretrained("microsoft/table-transformer-detection")
model.eval()

image = convert_from_path('/home/advait/expense-tracker/statement_unlocked.pdf')[0].convert("RGB")

inputs = processor(images=image, return_tensors="pt")
with torch.no_grad():
    outputs = model(**inputs)

target_sizes = torch.tensor([image.size[::-1]])
results = processor.post_process_object_detection(
    outputs, threshold=0.7, target_sizes=target_sizes
)[0]

# --- Visualise ---
fig, ax = plt.subplots(1, 1, figsize=(12, 16))
ax.imshow(image)

colors = {0: "red", 1: "blue"}  # 0=table, 1=table rotated (TATR label)
label_names = model.config.id2label

for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
    x1, y1, x2, y2 = box.tolist()
    label_id = label.item()
    color = colors.get(label_id, "green")

    rect = patches.Rectangle(
        (x1, y1), x2 - x1, y2 - y1,
        linewidth=2, edgecolor=color, facecolor="none"
    )
    ax.add_patch(rect)
    ax.text(
        x1, y1 - 5,
        f"{label_names[label_id]}: {score:.2f}",
        color=color, fontsize=10,
        bbox=dict(facecolor="white", alpha=0.6, edgecolor="none", pad=2)
    )

ax.axis("off")
plt.tight_layout()
plt.savefig("tatr_output.png", dpi=150, bbox_inches="tight")
plt.show()