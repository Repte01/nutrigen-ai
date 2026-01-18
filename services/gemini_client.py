import os
from dotenv import load_dotenv
import google.generativeai as genai

# Cargar variables de entorno
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")


def construir_prompt_nutricional(data: dict) -> str:
    return f"""
Eres un nutricionista profesional.

Genera un PLAN NUTRICIONAL SEMANAL.

Incluye desayuno, comida y cena para cada día.
Indica calorías aproximadas y consejos breves.

Objetivo: {data['objetivo']}
Restricciones: {data['restricciones']}
Alergias: {data['alergias']}
Ingredientes disponibles: {data['ingredientes']}
Observaciones: {data['observaciones']}

Devuelve el resultado en formato Markdown.
"""


def generar_respuesta(prompt: str) -> str:
    response = model.generate_content(prompt)
    return response.text
