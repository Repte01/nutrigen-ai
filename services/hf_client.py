# services/hf_client.py
import streamlit as st
import requests

HF_TOKEN = st.secrets["HUGGINGFACE_API_TOKEN"]

HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

MODEL = "HuggingFaceTB/SmolLM3-3B"

def hf_generate(prompt: str) -> str:
    # ✅ URL CORREGIDA
    url = f"https://router.huggingface.co/model/{MODEL}"
    
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 800,
            "temperature": 0.7,
            "top_p": 0.9,
            "return_full_text": False
        }
    }
    
    try:
        response = requests.post(
            url,
            headers=HEADERS,
            json=payload,
            timeout=120
        )
        
        if response.status_code == 404:
            return "❌ Error 404: Modelo no encontrado. Verifica la URL y el nombre del modelo."
        elif response.status_code != 200:
            return f"❌ Error HuggingFace ({response.status_code}): {response.text}"
        
        data = response.json()
        
        # Manejar diferentes formatos de respuesta
        if isinstance(data, list) and len(data) > 0:
            if "generated_text" in data[0]:
                return data[0]["generated_text"]
            elif "generated_text" in data:
                return data["generated_text"]
        
        return str(data)
        
    except requests.exceptions.Timeout:
        return "❌ Timeout: El modelo está cargando. Intenta de nuevo en 30 segundos."
    except Exception as e:
        return f"❌ Error de conexión: {str(e)}"
