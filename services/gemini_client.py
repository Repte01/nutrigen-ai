import streamlit as st
import google.generativeai as genai

# Configurar Gemini con la API Key desde Streamlit Secrets
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# ✅ MODELO CORRECTO
model = genai.GenerativeModel("models/gemini-1.5-flash")


def construir_prompt_nutricional(data: dict) -> str:
    return f"""
Eres un nutricionista profesional.

Genera un PLAN NUTRICIONAL SEMANAL claro y realista.

Incluye:
- Desayuno
- Comida
- Cena

Para cada día de la semana.
Añade calorías aproximadas y consejos breves.

Objetivo: {data['objetivo']}
Restricciones: {data['restricciones']}
Alergias: {data['alergias']}
Ingredientes disponibles: {data['ingredientes']}
Observaciones: {data['observaciones']}

Devuelve el resultado en formato Markdown.
"""


def generar_respuesta(prompt: str) -> str:
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Error con Gemini: {e}"
