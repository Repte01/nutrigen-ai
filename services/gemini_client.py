import os
from google import genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("❌ GEMINI_API_KEY no configurada")

client = genai.Client(api_key=GEMINI_API_KEY)


def gemini_chat(prompt: str) -> str:
    try:
        response = client.models.generate_content(
            model="models/gemini-1.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:
        raise Exception(f"Error Gemini: {e}")
