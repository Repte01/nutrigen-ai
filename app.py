import streamlit as st
from auth.login import login_form, register_form, logout
from services.gemini_client import gemini_chat

st.set_page_config("NutriGen AI", "🥗", layout="wide")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = None


# ---------- LOGIN ----------
if not st.session_state.logged_in:
    st.title("🥗 NutriGen AI")
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Registro"])

    with tab1:
        login_form()
    with tab2:
        register_form()

    st.stop()


# ---------- APP ----------
st.sidebar.success(f"👋 {st.session_state.user.email}")
st.sidebar.button("🚪 Cerrar sesión", on_click=logout)

section = st.sidebar.radio(
    "Secciones",
    ["🥗 Menús saludables", "🤖 Asistente IA", "💡 Hábitos saludables"]
)

st.title("🥗 NutriGen AI")

if section == "🤖 Asistente IA":
    st.header("🤖 Nutricionista con IA")

    prompt = st.text_area(
        "Describe tus objetivos y restricciones",
        height=150
    )

    if st.button("Generar plan"):
        with st.spinner("Pensando..."):
            respuesta = gemini_chat(prompt)

        st.success("Plan generado")
        st.markdown(respuesta)

elif section == "🥗 Menús saludables":
    st.header("🥗 Ejemplo de menú saludable")
    st.markdown("""
    - **Desayuno:** Avena con fruta  
    - **Comida:** Pollo con arroz  
    - **Cena:** Pescado con verduras  
    """)

elif section == "💡 Hábitos saludables":
    st.header("💡 Hábitos saludables")
    st.markdown("""
    - 🏃‍♂️ Ejercicio regular  
    - 💧 Hidratación  
    - 😴 Buen descanso  
    """)
