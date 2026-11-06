from mistralai.client import Mistral
from dotenv import load_dotenv
import os
from PIL import Image
import io
import base64
import asyncio
import yaml
from ollama import Client
import torch

load_dotenv()

with open('/home/advait/expense-tracker/backend/utils/prompts.yml', 'r') as f:
    prompts = yaml.safe_load(f)


config = {
    'api_key': os.environ["MISTRAL_API_KEY"],
    'vision_model': os.environ["MISTRAL_VISION_MODEL"]
}

llm = Mistral(config["api_key"])


def pil_to_base64(image: Image.Image, format: str = "JPEG") -> str:
    image = image.convert('RGB')
    buffered = io.BytesIO()
    image.save(buffered, format=format)
    return base64.b64encode(buffered.getvalue()).decode("utf-8")


async def send_image_to_mistral(images: list[Image.Image], system_prompt: str, human_prompt: str):
    model = config['vision_model']

    # Build user content (text + images)
    user_content = [{"type": "text", "text": human_prompt}]

    for img in images:
        b64_img = pil_to_base64(img)
        user_content.append({
            "type": "image_url",
            "image_url": f"data:image/jpeg;base64,{b64_img}"
        })

    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": user_content
        }
    ]

    response = await asyncio.to_thread(
        lambda: llm.chat.complete(model=model, messages=messages)
    )

    return response.choices[0].message.content


async def send_image_to_huggingfaceLM(
    images:list[Image.Image],
    system_prompt:str,
    human_prompt:str,
    model,
    processor
):

    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": [
                *[{
                    "type": "image",
                    "image": img.convert("RGB")
                } for img in images],
                {
                    "type": "text",
                    "text": human_prompt
                }
            ]
        }
    ]

    inputs = processor.apply_chat_template(
        messages,
        tokenize=True,
        add_generation_prompt=True,
        return_dict=True,
        return_tensors="pt",
        enable_thinking=False
    )
    inputs = {
        key: value.to(model.device) if torch.is_tensor(value) else value
        for key, value in inputs.items()
    }

    with torch.inference_mode():
        generated_ids = model.generate(
            **inputs,
            max_new_tokens=512
        )

    generated_ids = generated_ids[:, inputs["input_ids"].shape[1]:]

    response = processor.batch_decode(
        generated_ids,
        skip_special_tokens=True
    )[0]

    return response


async def send_image_to_ollama(
    images: Image.Image,
    system_prompt: str,
    human_prompt: str,
):
    client = Client(host="http://localhost:11434")

    messages = [
        {
            "role": "system",
            "content": system_prompt,
        },
        {
            "role": "user",
            "content": human_prompt,
            "images": [pil_to_base64(img) for img in images],
        },
    ]

    response = await asyncio.to_thread(
        lambda: client.chat(
            model="hf.co/bartowski/OpenGVLab_InternVL3_5-1B-GGUF:Q4_K_M",
            messages=messages,
            keep_alive=0,
            think=False
        )
    )

    return response