import google.generativeai as genai
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Configurar Gemini con la API Key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Usamos Gemini 1.5 Flash (rápido y gratuito)
model = genai.GenerativeModel("gemini-1.5-flash")


def construir_prompt_nutricional(data: dict) -> str:
    """
    Construye un prompt estructurado para generar
    un plan nutricional semanal personalizado.
    """
    return f"""
Eres un nutricionista profesional.

Genera un PLAN NUTRICIONAL SEMANAL completo y equilibrado.

Incluye para cada día:
- Desayuno
- Comida
- Cena

Datos del usuario:
Objetivo principal: {data['objetivo']}
Restricciones alimentarias: {data['restricciones']}
Alergias: {data['alergias']}
Ingredientes disponibles: {data['ingredientes']}
Observaciones adicionales: {data['observaciones']}

Requisitos:
- Usa únicamente ingredientes permitidos
- Evita completamente las alergias
- Indica calorías aproximadas por comida
- Da consejos nutricionales breves
- Usa formato Markdown claro y ordenado
"""


def generar_respuesta(prompt: str) -> str:
    """
    Envía el prompt a Gemini y devuelve la respuesta generada.
    """
    response = model.generate_content(prompt)
    return response.text
