import requests
import streamlit as st

API_KEY = st.secrets["GEMINI_API_KEY"]

# URL actualizada - usa gemini-1.5-pro o gemini-1.0-pro
URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.0-pro:generateContent"

def gemini_chat(prompt: str) -> str:
    headers = {
        'Content-Type': 'application/json',
    }
    
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.7,
            "topK": 1,
            "topP": 1,
            "maxOutputTokens": 2048,
        }
    }

    try:
        response = requests.post(
            f"{URL}?key={API_KEY}",
            headers=headers,
            json=payload,
            timeout=60
        )

        if response.status_code != 200:
            st.error(f"Error de API: {response.status_code}")
            st.code(response.text[:500])
            raise Exception(f"Gemini API error: {response.text}")

        data = response.json()
        
        # Extraer el texto de la respuesta
        if "candidates" in data and len(data["candidates"]) > 0:
            if "content" in data["candidates"][0]:
                return data["candidates"][0]["content"]["parts"][0]["text"]
        
        # Si la estructura es diferente
        return str(data)
        
    except requests.exceptions.RequestException as e:
        st.error(f"Error de conexión: {e}")
        raise Exception(f"Connection error: {e}")
