import os
import requests

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

API_URL = "https://api.groq.com/openai/v1/chat/completions"

def gemini_chat(prompt: str) -> str:
    if not GROQ_API_KEY:
        return "❌ Falta la GROQ_API_KEY en los secrets"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-70b-8192",  # ✅ MODELO ACTIVO
        "messages": [
            {
                "role": "system",
                "content": "Eres un nutricionista profesional y claro en tus explicaciones."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7
    }

    response = requests.post(API_URL, headers=headers, json=data)

    if response.status_code != 200:
        return f"❌ Error IA ({response.status_code}): {response.text}"

    return response.json()["choices"][0]["message"]["content"]
