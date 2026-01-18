import requests
import streamlit as st

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

API_URL = (
    "https://generativelanguage.googleapis.com/"
    "v1beta/models/gemini-1.5-flash:generateContent"
)


def gemini_chat(prompt: str) -> str:
    headers = {
        "Content-Type": "application/json"
    }

    body = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    response = requests.post(
        f"{API_URL}?key={GEMINI_API_KEY}",
        headers=headers,
        json=body,
        timeout=30
    )

    if response.status_code != 200:
        raise Exception(f"Gemini API error: {response.text}")

    data = response.json()
    return data["candidates"][0]["content"]["parts"][0]["text"]
