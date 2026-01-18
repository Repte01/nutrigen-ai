import streamlit as st
from google import genai
from google.genai import types

# Cliente Gemini (SDK NUEVO)
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

def gemini_chat(prompt: str) -> str:
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.7,
                max_output_tokens=1024
            )
        )

        return response.text

    except Exception as e:
        return f"❌ Error Gemini: {e}"
