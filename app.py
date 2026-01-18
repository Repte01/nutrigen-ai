import streamlit as st
from auth.login import login_form, register_form, logout
from services.gemini_client import gemini_chat

st.set_page_config(
    page_title="NutriGen AI",
    page_icon="🥗",
    layout="wide"
)

st.title("🥗 NutriGen AI")
st.caption("Tu asistente nutricional inteligente")

if "logged" not in st.session_state:
    st.session_state.logged = False

# ---------- LOGIN ----------
if not st.session_state.logged:
    c1, c2 = st.columns(2)
    with c1:
        login_form()
    with c2:
        register_form()
    st.stop()

st.success(f"👋 Bienvenido/a **{st.session_state.user.email}**")
st.button("🚪 Cerrar sesión", on_click=logout)

st.divider()

# ---------- NAVEGACIÓN ----------
page = st.radio(
    "📌 Secciones",
    ["🥗 Menús saludables", "🤖 Asistente IA", "💡 Hábitos saludables"],
    horizontal=True
)

# ================= MENÚS =================
if page == "🥗 Menús saludables":
    st.header("🍽️ Menús equilibrados")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🏃 Menú para energía")
        st.table({
            "Comida": ["Desayuno", "Comida", "Cena"],
            "Plato": [
                "Avena + fruta",
                "Pollo con arroz integral",
                "Pescado con verduras"
            ]
        })

    with col2:
        st.subheader("🔥 Menú para adelgazar")
        st.table({
            "Comida": ["Desayuno", "Comida", "Cena"],
            "Plato": [
                "Yogur + nueces",
                "Ensalada con legumbres",
                "Tortilla francesa"
            ]
        })

# ================= CHAT IA =================
elif page == "🤖 Asistente IA":
    st.header("🤖 Nutricionista con IA")

    st.info("Describe tus objetivos, alergias y preferencias")

    prompt = st.text_area(
        "📝 Ejemplo: Quiero ganar músculo, soy celíaco y alérgico a las nueces",
        height=150
    )

    if st.button("✨ Generar plan nutricional"):
        with st.spinner("🧠 Pensando..."):
            respuesta = gemini_chat(prompt)

        st.success("✅ Plan generado")
        st.markdown(respuesta)

# ================= HÁBITOS =================
elif page == "💡 Hábitos saludables":
    st.header("🌱 Mejora tu salud día a día")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("🚶 Pasos diarios", "8.000")
        st.write("Caminar mejora el sistema cardiovascular")

    with col2:
        st.metric("💧 Agua", "2L / día")
        st.write("Hidratación = mejor rendimiento")

    with col3:
        st.metric("😴 Sueño", "7-8h")
        st.write("Dormir bien regula hormonas")

    with st.expander("📚 Consejos extra"):
        st.markdown("""
        - 🏃 Haz deporte 3 veces por semana  
        - 🥦 Come variado  
        - 🧘 Reduce el estrés  
        - ⏰ Mantén horarios regulares  
        """)
