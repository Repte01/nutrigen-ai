import os
from google import genai

# Cliente oficial nuevo
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def gemini_chat(prompt: str) -> str:
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:
        raise Exception(f"Error Gemini API: {e}")
