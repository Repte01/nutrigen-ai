import requests
import streamlit as st

API_KEY = st.secrets["GEMINI_API_KEY"]

def gemini_chat(prompt: str) -> str:
    url = (
        "https://generativelanguage.googleapis.com/v1/models/"
        f"gemini-pro:generateContent?key={API_KEY}"
    )

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    try:
        response = requests.post(
            url,
            json=payload,
            timeout=60
        )

        if response.status_code != 200:
            return f"❌ Error Gemini ({response.status_code}): {response.text}"

        data = response.json()

        return data["candidates"][0]["content"]["parts"][0]["text"]

    except Exception as e:
        return f"❌ Error al conectar con Gemini: {e}"
