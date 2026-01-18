import streamlit as st
from auth.login import login_form, register_form, logout
from services.gemini_client import gemini_chat

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

# ----------------------------------
# MENÚS SALUDABLES
# ----------------------------------
if seccion == "🥗 Menús saludables":
    st.header("🥗 Menús saludables")

    st.table({
        "Comida": ["Desayuno", "Comida", "Cena"],
        "Ejemplo saludable": [
            "Avena con fruta y yogur",
            "Pollo con arroz y verduras",
            "Pescado al horno con ensalada"
        ]
    })

    st.info("Menús orientativos para una dieta equilibrada.")

# ----------------------------------
# ASISTENTE IA
# ----------------------------------
elif seccion == "🤖 Asistente IA":
    st.header("🤖 Nutricionista con IA")

    prompt = st.text_area(
        "Describe tus objetivos, alergias y preferencias",
        placeholder="Quiero ganar músculo, soy celíaco y alérgico a las nueces",
        height=160
    )

    if st.button("✨ Generar plan nutricional"):
        if not prompt.strip():
            st.warning("Escribe algo primero")
        else:
            with st.spinner("🧠 Generando plan..."):
                respuesta = gemini_chat(prompt)

            st.success("✅ Plan generado")
            st.markdown(respuesta)

# ----------------------------------
# HÁBITOS SALUDABLES
# ----------------------------------
elif seccion == "💡 Hábitos saludables":
    st.header("💡 Hábitos saludables")

    st.markdown("""
    - 🏃‍♂️ Actividad física regular  
    - 💧 Beber suficiente agua  
    - 😴 Dormir entre 7 y 9 horas  
    - 🥗 Comer variado y equilibrado  
    - 🧘 Reducir el estrés  
    """)

    st.success("La constancia es la clave de una buena salud.")

st.caption("NutriGen AI · Proyecto educativo · IA aplicada a la nutrición")
