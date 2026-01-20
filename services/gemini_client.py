import os
from google import genai
from google.genai.errors import ServerError


def gemini_chat(prompt: str) -> str:
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise Exception("❌ GEMINI_API_KEY no encontrada")

    client = genai.Client(api_key=api_key)

    try:
        # Intento con modelo rápido
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt
        )
        return response.text

    except ServerError:
        # Fallback automático a modelo estable
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )
        return response.text
