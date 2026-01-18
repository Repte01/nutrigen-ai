import streamlit as st
from google import genai

# Crear cliente oficial (SDK NUEVO)
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])


def gemini_chat(prompt: str) -> str:
    try:
        response = client.models.generate_content(
            model="gemini-1.5-pro",
            contents=prompt
        )
        return response.text
    except Exception as e:
        raise Exception(f"Error Gemini API: {e}")
