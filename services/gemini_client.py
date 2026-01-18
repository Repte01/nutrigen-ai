import requests
import streamlit as st

def gemini_chat(prompt: str) -> str:
    api_key = st.secrets.get("GROQ_API_KEY")

    if not api_key:
        return "❌ No se ha encontrado la GROQ_API_KEY en Secrets."

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {
                "role": "system",
                "content": (
                    "Eres un nutricionista profesional. "
                    "Generas menús saludables, planes semanales, "
                    "hábitos saludables y consejos claros."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        return f"❌ Error IA ({response.status_code}): {response.text}"

    return response.json()["choices"][0]["message"]["content"]
