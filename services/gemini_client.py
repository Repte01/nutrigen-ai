import os
import streamlit as st
import google.generativeai as genai


# -------------------------
# CONFIGURACIÓN API KEY
# -------------------------
GEMINI_API_KEY = None

# Streamlit Cloud
if hasattr(st, "secrets"):
    GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY")

# Local .env
if not GEMINI_API_KEY:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("❌ GEMINI_API_KEY no encontrada")

genai.configure(api_key=GEMINI_API_KEY)


# -------------------------
# MODELO (CORRECTO)
# -------------------------
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash"
)


# -------------------------
# FUNCIÓN PRINCIPAL
# -------------------------
def generar_respuesta(prompt: str) -> str:
    """
    Envía un prompt de texto a Gemini y devuelve la respuesta generada.
    """
    try:
        response = model.generate_content(prompt)

        if not response or not response.text:
            return "❌ Gemini no devolvió respuesta."

        return response.text

    except Exception as e:
        return f"❌ Error al generar el plan nutricional: {e}"
