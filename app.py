import streamlit as st
from auth.login import login_form, register_form, logout
from services.gemini_client import gemini_chat

st.set_page_config(page_title="NutriGen AI", layout="wide")

st.title("🥗 NutriGen AI")
st.caption("Planes nutricionales con IA")

if "logged" not in st.session_state:
    st.session_state.logged = False


# ---------------- LOGIN ----------------
if not st.session_state.logged:
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Registro"])
    with tab1:
        login_form()
    with tab2:
        register_form()
    st.stop()


st.success(f"Bienvenido/a {st.session_state.user.email}")
st.button("Cerrar sesión", on_click=logout)

# ---------------- SLIDES ----------------
slide = st.radio(
    "Navegación",
    ["🥗 Menús saludables", "🤖 Asistente IA", "💡 Hábitos saludables"],
    horizontal=True
)

# ---------- SLIDE 1 ----------
if slide == "🥗 Menús saludables":
    st.header("🍽️ Ejemplos de menús saludables")

    st.markdown("""
    **Desayuno:** Avena con fruta y yogur  
    **Comida:** Pollo con arroz integral y verduras  
    **Cena:** Pescado al horno con ensalada  
    """)

# ---------- SLIDE 2 ----------
elif slide == "🤖 Asistente IA":
    st.header("🤖 Chat nutricional personalizado")

    if "chat" not in st.session_state:
        st.session_state.chat = ""

    user_input = st.text_area("Cuéntame tus objetivos, restricciones e ingredientes")

    if st.button("Generar plan"):
        with st.spinner("Generando plan..."):
            respuesta = gemini_chat(user_input)
            st.session_state.chat = respuesta

    if st.session_state.chat:
        st.markdown(st.session_state.chat)

# ---------- SLIDE 3 ----------
elif slide == "💡 Hábitos saludables":
    st.header("🌱 Mejora tu salud")

    st.markdown("""
    - 🚶 Caminar 30 min al día  
    - 🏃 Hacer deporte 3 veces por semana  
    - 💧 Beber agua suficiente  
    - 😴 Dormir 7–8 horas  
    - 🥦 Comer variado y equilibrado  
    """)
