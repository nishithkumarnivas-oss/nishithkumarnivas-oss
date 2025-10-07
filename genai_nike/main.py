import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import openai
import httpx
from .brand_config import BRAND

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
STABLE_DIFFUSION_API_KEY = os.getenv("STABLE_DIFFUSION_API_KEY")

openai.api_key = OPENAI_API_KEY

app = FastAPI(title="Nike GenAI Agent")

class PromptRequest(BaseModel):
    prompt: str
    asset_type: str  # 'copy' or 'image'

@app.post("/generate")
async def generate_asset(req: PromptRequest):
    if req.asset_type == "copy":
        return {"result": await generate_copy(req.prompt)}
    elif req.asset_type == "image":
        image_url = await generate_image(req.prompt)
        return {"result": image_url}
    else:
        raise HTTPException(status_code=400, detail="Invalid asset_type. Use 'copy' or 'image'.")

async def generate_copy(prompt: str) -> str:
    system_prompt = f"You are a Nike brand copywriter. Use the slogan '{BRAND['slogan']}' and Nike's bold, motivational tone. Colors: {BRAND['colors']}." 
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message['content'].strip()

async def generate_image(prompt: str) -> str:
    # Example using Stability AI's Stable Diffusion API
    headers = {"Authorization": f"Bearer {STABLE_DIFFUSION_API_KEY}"}
    payload = {
        "prompt": f"{prompt}, Nike style, colors: black, white, red, logo, bold, modern",
        "width": 512,
        "height": 512,
        "steps": 30
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.stability.ai/v1/generation/stable-diffusion-v1-5/text-to-image",
            headers=headers,
            json=payload
        )
        if response.status_code == 200:
            data = response.json()
            return data.get("artifacts", [{}])[0].get("url", "")
        else:
            raise HTTPException(status_code=500, detail="Image generation failed.")
