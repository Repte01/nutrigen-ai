# services/hf_client.py
import streamlit as st
import requests

HF_TOKEN = st.secrets["HUGGINGFACE_API_TOKEN"]
HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

# ✅ NUEVO MODELO - SmolLM3-3B
MODEL = "HuggingFaceTB/SmolLM3-3B"

def hf_generate(prompt: str, enable_thinking: bool = False) -> str:
    # URL correcta para la API de inferencia
    url = f"https://router.huggingface.co/models/{MODEL}"
    
    # 🔧 Aprovecha las características del modelo: estructura el prompt para chat
    messages = [
        {"role": "user", "content": prompt}
    ]
    
    # Construye el prompt con el formato que espera el modelo
    chat_prompt = f"<|user|>\n{prompt}\n<|assistant|>\n"
    
    payload = {
        "inputs": chat_prompt,
        "parameters": {
            "max_new_tokens": 1500,  # Aumentado para respuestas más completas
            "temperature": 0.6,      # Recomendado por los autores del modelo
            "top_p": 0.95,           # Recomendado por los autores
            "return_full_text": False,
            "do_sample": True
        }
    }
    
    # Si quieres desactivar el modo "thinking" (razonamiento extendido)
    if not enable_thinking:
        # Puedes añadir una instrucción al sistema
        system_instruction = "/no_think\n"
        chat_prompt = f"<|system|>\n{system_instruction}<|user|>\n{prompt}\n<|assistant|>\n"
        payload["inputs"] = chat_prompt

    try:
        response = requests.post(
            url,
            headers=HEADERS,
            json=payload,
            timeout=45  # Un poco más de tiempo para modelos más grandes
        )
        
        if response.status_code == 503:
            # Modelo cargándose - común con modelos recién usados
            return "🔄 El modelo se está cargando. Por favor, intenta de nuevo en 20-30 segundos."
        elif response.status_code != 200:
            return f"❌ Error ({response.status_code}): {response.text[:200]}"
        
        data = response.json()
        
        # Extrae la respuesta del formato de la API
        if isinstance(data, list) and len(data) > 0:
            if "generated_text" in data[0]:
                return data[0]["generated_text"].strip()
        
        # Formato alternativo
        if isinstance(data, dict) and "generated_text" in data:
            return data["generated_text"].strip()
            
        return str(data)[:2000]  # Limita la respuesta si viene en formato inesperado
        
    except requests.exceptions.Timeout:
        return "⏱️ La solicitud tardó demasiado. El modelo podría estar muy ocupado."
    except Exception as e:
        return f"❌ Error de conexión: {str(e)}"
