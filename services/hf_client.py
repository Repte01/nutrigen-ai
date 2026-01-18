import os
import streamlit as st
import requests

API_TOKEN = st.secrets["HUGGINGFACE_API_TOKEN"]

HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}"
}

def hf_generate(prompt: str, model="mistralai/Mistral-7B-Instruct") -> str:
    url = f"https://api-inference.huggingface.co/models/{model}"

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 512
        }
    }

    response = requests.post(url, headers=HEADERS, json=payload, timeout=100)

    if response.status_code != 200:
        return f"❌ Error HuggingFace: {response.status_code} - {response.text}"

    data = response.json()
    # Puede devolver texto directamente o como lista,
    # dependiendo del modelo
    if isinstance(data, list):
        # Texto en data[0]["generated_text"]
        return data[0].get("generated_text", "")
    elif isinstance(data, dict) and "generated_text" in data:
        return data["generated_text"]
    else:
        # Fallback a texto plano
        return str(data)
