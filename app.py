import streamlit as st
from auth.login import login_form, register_form, logout
from services.gemini_client import gemini_chat
from services.chat_service import save_chat, get_chat_history, update_chat_title
from services.pdf_reader_service import pdf_to_text
from services.pdf_chat_service import save_pdf_chat, get_pdf_chat_history

# ---------------- CONFIG ----------------
st.set_page_config("NutriGen AI", "🥗", layout="wide")

# ---------------- SESSION STATE ----------------
st.session_state.setdefault("logged_in", False)
st.session_state.setdefault("pdf_text", None)
st.session_state.setdefault("pdf_name", None)

# ---------------- LOGIN ----------------
if not st.session_state.logged_in:
    st.title("🥗 NutriGen AI")
    tab1, tab2 = st.tabs(["Login", "Registro"])
    with tab1:
        login_form()
    with tab2:
        register_form()
    st.stop()

# ---------------- APP ----------------
st.title("🥗 NutriGen AI")
st.sidebar.button("Cerrar sesión", on_click=logout)

seccion = st.sidebar.radio(
    "Secciones",
    ["Menús", "Asistente IA", "PDF", "Hábitos"]
)

# =================================================
# 🥗 MENÚS
# =================================================
if seccion == "Menús":
    st.header("🥗 Menús saludables")

    st.table({
        "Comida": ["Desayuno", "Comida", "Cena"],
        "Ejemplo": [
            "Avena con fruta",
            "Pollo con arroz",
            "Pescado con ensalada"
        ]
    })

# =================================================
# 🤖 ASISTENTE IA
# =================================================
elif seccion == "Asistente IA":
    st.header("🤖 Plan nutricional con IA")

    objetivos = st.multiselect(
        "Objetivos",
        [
            "Perder grasa",
            "Ganar masa muscular",
            "Ganar peso",
            "Mantener peso"
        ]
    )

    implicacion = st.slider("Nivel de implicación", 1, 3, 2)
    observaciones = st.text_area("Observaciones")

    prompt = f"""
Eres un nutricionista profesional.

Objetivos: {', '.join(objetivos)}
Nivel de implicación: {implicacion}/3
Observaciones: {observaciones}

Genera un plan nutricional claro y realista.
"""

    if st.button("Generar plan"):
        respuesta = gemini_chat(prompt)
        save_chat(st.session_state.user.id, prompt, respuesta)
        st.markdown(respuesta)

    st.divider()
    st.subheader("Historial")

    for chat in get_chat_history(st.session_state.user.id):
        titulo = chat.get("titulo") or "Plan nutricional"

        with st.expander(titulo):
            nuevo = st.text_input(
                "Renombrar",
                titulo,
                key=f"t_{chat['id']}"
            )
            if nuevo != titulo:
                update_chat_title(chat["id"], nuevo)
                st.rerun()

            st.markdown(chat["respuesta"])

# =================================================
# 📄 PDF
# =================================================
elif seccion == "PDF":
    st.header("📄 Analizar menú PDF")

    pdf = st.file_uploader("Sube un PDF", type="pdf")

    if pdf:
        st.session_state.pdf_name = pdf.name
        if not st.session_state.pdf_text:
            st.session_state.pdf_text = pdf_to_text(pdf)

        pregunta = st.text_input("Pregunta sobre el menú")

        if st.button("Preguntar") and pregunta:
            prompt = f"{st.session_state.pdf_text}\n\nPregunta: {pregunta}"
            respuesta = gemini_chat(prompt)

            save_pdf_chat(
                st.session_state.user.id,
                st.session_state.pdf_name,
                pregunta,
                respuesta
            )

            st.markdown(respuesta)

        for chat in get_pdf_chat_history(
            st.session_state.user.id,
            st.session_state.pdf_name
        ):
            with st.expander(chat["pregunta"]):
                st.markdown(chat["respuesta"])

# =================================================
# 💡 HÁBITOS
# =================================================
elif seccion == "Hábitos":
    st.header("💡 Hábitos saludables")

    st.markdown("""
- 🏃 Actividad física regular  
- 💧 Beber agua suficiente  
- 😴 Dormir bien  
""")

# ---------------- FOOTER ----------------
st.caption("NutriGen AI · Proyecto educativo")
