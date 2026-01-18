import requests
import streamlit as st

API_KEY = st.secrets["GEMINI_API_KEY"]

URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

def gemini_chat(prompt: str) -> str:
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    response = requests.post(
        f"{URL}?key={API_KEY}",
        json=payload,
        timeout=30
    )

    if response.status_code != 200:
        raise Exception(f"Gemini API error: {response.text}")

    data = response.json()
    return data["candidates"][0]["content"]["parts"][0]["text"]
