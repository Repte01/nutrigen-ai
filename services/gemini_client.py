import requests
import streamlit as st
import json
from typing import Optional

API_KEY = st.secrets["GEMINI_API_KEY"]

def gemini_chat(prompt: str, max_tokens: int = 2000) -> str:
    """
    Envía un prompt a Gemini API y retorna la respuesta.
    
    Args:
        prompt: El texto a enviar a la IA
        max_tokens: Máximo de tokens en la respuesta
        
    Returns:
        Respuesta de la IA o mensaje de error
    """
    url = (
        "https://generativelanguage.googleapis.com/v1/models/"
        f"gemini-pro:generateContent?key={API_KEY}"
    )

    # Configurar el prompt para respuestas estructuradas
    structured_prompt = f"""
    Eres NutriGen AI, un asistente nutricional experto. 
    Responde de manera clara, estructurada y amigable.
    Usa emojis relevantes para hacer la respuesta visual.
    Organiza la información en secciones claras.
    
    Pregunta del usuario:
    {prompt}
    
    Por favor, proporciona una respuesta completa y útil:
    """
    
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": structured_prompt}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.7,
            "topK": 40,
            "topP": 0.95,
            "maxOutputTokens": max_tokens,
            "stopSequences": []
        },
        "safetySettings": [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            }
        ]
    }

    try:
        response = requests.post(
            url,
            json=payload,
            timeout=120,  # Aumentado a 2 minutos para respuestas largas
            headers={
                "Content-Type": "application/json"
            }
        )

        if response.status_code == 200:
            data = response.json()
            
            # Verificar que hay contenido
            if "candidates" in data and len(data["candidates"]) > 0:
                if "content" in data["candidates"][0]:
                    text = data["candidates"][0]["content"]["parts"][0]["text"]
                    
                    # Limpiar respuesta si es necesario
                    text = text.replace("**", "**")  # Mantener formato markdown
                    
                    # Asegurar que la respuesta no esté vacía
                    if text.strip():
                        return text
                    else:
                        return "🤖 La IA generó una respuesta vacía. Por favor, intenta con más detalles."
            
            return "❌ La respuesta de la IA no tiene el formato esperado."
            
        elif response.status_code == 429:
            return "⚠️ Demasiadas solicitudes. Por favor, espera unos momentos antes de intentar de nuevo."
            
        elif response.status_code == 400:
            error_data = response.json()
            return f"❌ Error en la solicitud: {error_data.get('error', {}).get('message', 'Error desconocido')}"
            
        else:
            return f"❌ Error Gemini ({response.status_code}): {response.text[:200]}"

    except requests.exceptions.Timeout:
        return "⏱️ La solicitud tardó demasiado tiempo. Por favor, intenta con un prompt más corto o específico."
        
    except requests.exceptions.ConnectionError:
        return "🔌 Error de conexión. Verifica tu internet e intenta nuevamente."
        
    except Exception as e:
        return f"❌ Error inesperado al conectar con Gemini: {str(e)[:200]}"
