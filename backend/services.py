from fastapi import FastAPI, HTTPException, Body
import httpx

OPENAI_API_KEY = "Kk7fE8SmGjbaOrX44apbT3BlbkFJ3FLd8KlBdX8otY9p3bS7"
OPENAI_API_URL = "https://api.openai.com/v1/completions"

async def send_prompt_to_chatgpt(prompt_text: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            OPENAI_API_URL,
            json={
                "model": "gpt-4-turbo-preview",
                "prompt": prompt_text,
                "max_tokens": 150  # Adjust based on your needs
            },
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}"
            }
        )
        response.raise_for_status()
        return response.json()