import streamlit as st
import requests

HF_TOKEN = st.secrets["HUGGINGFACE_API_TOKEN"]

HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

# ✅ MODELO GRATUITO Y COMPATIBLE
MODEL = "HuggingFaceH4/zephyr-7b-beta"

def hf_generate(prompt: str) -> str:
    url = f"https://router.huggingface.co/hf-inference/models/{MODEL}"

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

        if response.status_code != 200:
            return f"❌ Error HuggingFace ({response.status_code}): {response.text}"

        data = response.json()

        if isinstance(data, list) and "generated_text" in data[0]:
            return data[0]["generated_text"]

        return str(data)

    except Exception as e:
        return f"❌ Error de conexión con HuggingFace: {e}"
