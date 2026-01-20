import streamlit as st
from auth.login import login_form, register_form, logout
from services.gemini_client import gemini_chat
from services.chat_service import (
    save_chat,
    get_chat_history,
    update_chat_title,
    append_to_chat
)
from services.pdf_service import generar_pdf_chat

# ----------------------------------
# Configuración
# ----------------------------------
st.set_page_config(
    page_title="NutriGen AI",
    page_icon="🥗",
    layout="wide"
)

# ----------------------------------
# Estado de sesión
# ----------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ----------------------------------
# LOGIN / REGISTRO
# ----------------------------------
if not st.session_state.logged_in:
    st.title("🥗 NutriGen AI")
    st.subheader("Planes nutricionales con Inteligencia Artificial")

    tab1, tab2 = st.tabs(["🔐 Login", "📝 Registro"])

    with tab1:
        login_form()

    with tab2:
        register_form()

    st.stop()

# ----------------------------------
# APP PRINCIPAL
# ----------------------------------
st.title("🥗 NutriGen AI")
st.subheader("Tu asistente nutricional inteligente")

st.sidebar.button("🚪 Cerrar sesión", on_click=logout)

st.sidebar.title("📌 Secciones")
seccion = st.sidebar.radio(
    "Ir a:",
    [
        "🥗 Menús saludables",
        "🤖 Asistente IA",
        "💡 Hábitos saludables"
    ]
)

# ======================================================
# 🤖 ASISTENTE IA
# ======================================================
if seccion == "🤖 Asistente IA":
    st.header("🤖 Nutricionista con IA")

    col1, col2 = st.columns(2)

    with col1:
        objetivo = st.selectbox(
            "🎯 Objetivo principal",
            [
                "Ganar masa muscular",
                "Perder grasa",
                "Mantener peso",
                "Mejorar salud general",
                "Rendimiento deportivo"
            ]
        )

        implicacion = st.slider("⚖️ Nivel de implicación", 1, 3, 2)
        alergias = st.multiselect("🚫 Alergias", ["Nueces", "Gluten", "Lactosa", "Huevo", "Marisco"])
        restricciones = st.multiselect("🥦 Restricciones", ["Vegetariano", "Vegano", "Sin gluten", "Sin lactosa", "Keto"])

    with col2:
        observaciones = st.text_area("📝 Información adicional", height=180)

    prompt = f"""
Eres un nutricionista profesional.

Objetivo: {objetivo}
Nivel de implicación: {implicacion}/3
Alergias: {', '.join(alergias) if alergias else 'Ninguna'}
Restricciones: {', '.join(restricciones) if restricciones else 'Ninguna'}
Observaciones: {observaciones if observaciones else 'Ninguna'}

Genera un plan claro y práctico.
"""

    st.code(prompt)

    if st.button("✨ Generar plan"):
        with st.spinner("🧠 Generando plan..."):
            respuesta = gemini_chat(prompt)
            save_chat(st.session_state.user.id, prompt, respuesta)
        st.success("Plan generado")

    # ---------------- HISTORIAL ----------------
    st.divider()
    st.subheader("🕒 Historial")

    historial = get_chat_history(st.session_state.user.id)

    for chat in historial:
        titulo = chat.get("titulo") or "Plan nutricional"

        with st.expander(f"🗂 {titulo} · {chat['created_at']}"):
            nuevo_titulo = st.text_input(
                "✏️ Renombrar",
                value=titulo,
                key=f"t_{chat['id']}"
            )

            if nuevo_titulo != titulo:
                update_chat_title(chat["id"], nuevo_titulo)
                st.rerun()

            st.markdown(chat["respuesta"])

            # ---- CONTINUAR CONVERSACIÓN ----
            pregunta = st.text_input(
                "💬 Pregunta sobre este plan",
                key=f"q_{chat['id']}"
            )

            if st.button("Enviar", key=f"b_{chat['id']}") and pregunta:
                contexto = f"""
Esta es la conversación hasta ahora:

{chat['respuesta']}

El usuario pregunta:
{pregunta}
"""
                respuesta_ia = gemini_chat(contexto)
                append_to_chat(chat["id"], chat["respuesta"], pregunta, respuesta_ia)
                st.rerun()

            pdf = generar_pdf_chat(chat["prompt"], chat["respuesta"])
            st.download_button(
                "📄 Exportar PDF",
                data=pdf,
                file_name="nutrigen_chat.pdf",
                mime="application/pdf"
            )
