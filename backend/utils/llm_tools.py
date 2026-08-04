from mistralai.client import Mistral
from dotenv import load_dotenv
import os
from PIL import Image
import io
import base64
import asyncio
import yaml
from ollama import Client


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


async def send_image_to_ollama(
    images,
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
            model="gemma4:e4b",
            messages=messages,
            keep_alive=0
        )
    )

    return response["message"]["content"]