import streamlit as st
from auth.login import login_form, register_form, logout
from services.gemini_client import gemini_chat

# ----------------------------------
# CONFIGURACIÓN + TEMA OSCURO
# ----------------------------------
st.set_page_config(
    page_title="NutriGen AI",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
body {
    background-color: #0e1117;
    color: #fafafa;
}
.section-card {
    background-color: #161b22;
    padding: 24px;
    border-radius: 14px;
    margin-bottom: 20px;
}
.section-title {
    color: #2ecc71;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------------
# ESTADO DE SESIÓN
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
        "🤖 Asistente IA",
        "🥗 Menús saludables",
        "💡 Hábitos saludables"
    ]
)

# ======================================================
# 🤖 ASISTENTE IA
# ======================================================
if seccion == "🤖 Asistente IA":
    st.markdown("<h2 class='section-title'>🤖 Nutricionista con IA</h2>", unsafe_allow_html=True)
    st.write("Configura tu plan nutricional de forma visual y personalizada.")

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

        implicacion = st.slider(
            "⚖️ Nivel de implicación",
            min_value=1,
            max_value=3,
            value=2,
            help="1 = Flexible · 3 = Muy estricto"
        )

        alergias = st.multiselect(
            "🚫 Alergias",
            ["Gluten", "Lactosa", "Huevo", "Nueces", "Marisco"]
        )

    with col2:
        observaciones = st.text_area(
            "📝 Información adicional",
            placeholder="Entreno, horarios, preferencias, tiempo para cocinar...",
            height=180
        )

    prompt = f"""
Eres un nutricionista profesional.

Objetivo: {objetivo}
Nivel de implicación: {implicacion}/3
Alergias: {', '.join(alergias) if alergias else 'Ninguna'}
Observaciones: {observaciones if observaciones else 'Ninguna'}

Genera un plan nutricional con:
- Menú orientativo
- Calorías aproximadas
- Consejos prácticos
"""

    st.markdown("### 📄 Prompt generado automáticamente")
    st.code(prompt)

    if st.button("✨ Generar plan nutricional"):
        with st.spinner("🧠 Generando plan..."):
            respuesta = gemini_chat(prompt)

        st.success("✅ Plan generado")
        st.markdown(respuesta)

# ======================================================
# 🥗 MENÚS SALUDABLES
# ======================================================
elif seccion == "🥗 Menús saludables":
    st.markdown("<h2 class='section-title'>🥗 Menús saludables</h2>", unsafe_allow_html=True)
    st.write("Ejemplos de menús equilibrados para el día a día.")

    desayuno, comida, cena = st.tabs(["🍳 Desayunos", "🍛 Comidas", "🍽️ Cenas"])

    with desayuno:
        st.markdown("""
        - Avena con fruta y yogur  
        - Tostadas integrales con aceite de oliva  
        - Huevos revueltos con fruta  
        """)

    with comida:
        st.markdown("""
        - Pollo con arroz y verduras  
        - Lentejas con verduras  
        - Pasta integral con atún  
        """)

    with cena:
        st.markdown("""
        - Pescado al horno con ensalada  
        - Tortilla francesa con espinacas  
        - Crema de verduras  
        """)

    st.info("💡 Ajusta cantidades según tu objetivo y actividad física.")

# ======================================================
# 💡 HÁBITOS SALUDABLES
# ======================================================
elif seccion == "💡 Hábitos saludables":
    st.markdown("<h2 class='section-title'>💡 Hábitos saludables</h2>", unsafe_allow_html=True)
    st.write("Pequeñas acciones diarias que mejoran tu salud.")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("🏃 Movimiento")
        st.markdown("""
        - Caminar 30 min diarios  
        - Entrenar fuerza  
        - Estiramientos  
        """)

    with col2:
        st.subheader("💧 Hidratación")
        st.markdown("""
        - 1.5–2L de agua  
        - Evitar refrescos  
        - Beber antes de comer  
        """)

    with col3:
        st.subheader("😴 Descanso")
        st.markdown("""
        - Dormir 7–9 horas  
        - Rutina regular  
        - Menos pantallas  
        """)

    st.success("🌱 La constancia vale más que la perfección.")

# ----------------------------------
st.caption("NutriGen AI · Proyecto educativo · IA aplicada a la nutrición")
