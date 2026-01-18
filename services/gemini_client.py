import streamlit as st
import google.generativeai as genai

# Configurar API Key
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# ⚠️ MODELO COMPATIBLE
model = genai.GenerativeModel("gemini-pro")


def gemini_chat(prompt: str) -> str:
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        raise Exception(f"Error Gemini SDK: {e}")
