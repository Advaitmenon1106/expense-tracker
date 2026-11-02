from transformers import BitsAndBytesConfig
from transformers import AutoModel, AutoTokenizer
import torch

model_id = "OpenGVLab/InternVL3_5-1B-Instruct"

quant_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
)

model = AutoModel.from_pretrained(
    model_id,
    quantization_config=quant_config,
    torch_dtype=torch.float16,
    trust_remote_code=True,
).eval()

tokenizer = AutoTokenizer.from_pretrained(
    model_id,
    trust_remote_code=True,
)