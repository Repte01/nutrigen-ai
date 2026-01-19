import streamlit as st
from auth.login import login_form, register_form, logout
from services.gemini_client import gemini_chat

# ----------------------------------
# CONFIG + TEMA OSCURO
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
.metric-card {
    background-color: #161b22;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
}
.metric-title {
    font-size: 14px;
    color: #8b949e;
}
.metric-value {
    font-size: 28px;
    color: #2ecc71;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------------
# ESTADO GLOBAL
# ----------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "historial_planes" not in st.session_state:
    st.session_state.historial_planes = []

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
        "📊 Dashboard",
        "🤖 Asistente IA",
        "📚 Historial",
        "🥗 Menús saludables",
        "💡 Hábitos saludables"
    ]
)

# ======================================================
# 📊 DASHBOARD
# ======================================================
if seccion == "📊 Dashboard":
    st.header("📊 Tu progreso")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-title">Planes generados</div>
            <div class="metric-value">{}</div>
        </div>
        """.format(len(st.session_state.historial_planes)), unsafe_allow_html=True)

    with col2:
        objetivo_actual = (
            st.session_state.historial_planes[-1]["objetivo"]
            if st.session_state.historial_planes else "—"
        )
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Último objetivo</div>
            <div class="metric-value">{objetivo_actual}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        nivel = (
            st.session_state.historial_planes[-1]["implicacion"]
            if st.session_state.historial_planes else "—"
        )
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Implicación</div>
            <div class="metric-value">{nivel}</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.info("📈 El progreso se basa en constancia y generación de planes.")

# ======================================================
# 🤖 ASISTENTE IA
# ======================================================
elif seccion == "🤖 Asistente IA":
    st.header("🤖 Nutricionista con IA")

    col1, col2 = st.columns(2)

    with col1:
        objetivo = st.selectbox(
            "🎯 Objetivo",
            [
                "Ganar masa muscular",
                "Perder grasa",
                "Mantener peso",
                "Mejorar salud",
                "Rendimiento deportivo"
            ]
        )

        implicacion = st.slider(
            "⚖️ Nivel de implicación",
            1, 3, 2,
            help="1 = flexible · 3 = muy estricto"
        )

        alergias = st.multiselect(
            "🚫 Alergias",
            ["Gluten", "Lactosa", "Huevo", "Nueces", "Marisco"]
        )

    with col2:
        observaciones = st.text_area(
            "📝 Información adicional",
            placeholder="Entreno, horarios, preferencias...",
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

    if st.button("✨ Generar plan"):
        with st.spinner("🧠 Generando plan..."):
            respuesta = gemini_chat(prompt)

        st.success("✅ Plan generado")
        st.markdown(respuesta)

        st.session_state.historial_planes.append({
            "objetivo": objetivo,
            "implicacion": implicacion,
            "respuesta": respuesta
        })

# ======================================================
# 📚 HISTORIAL
# ======================================================
elif seccion == "📚 Historial":
    st.header("📚 Historial de planes")

    if not st.session_state.historial_planes:
        st.info("Aún no has generado ningún plan.")
    else:
        for i, plan in enumerate(reversed(st.session_state.historial_planes), 1):
            with st.expander(f"📄 Plan {i} — {plan['objetivo']}"):
                st.markdown(plan["respuesta"])

# ======================================================
# 🥗 MENÚS
# ======================================================
elif seccion == "🥗 Menús saludables":
    st.header("🥗 Menús saludables")

    desayuno, comida, cena = st.tabs(["🍳 Desayunos", "🍛 Comidas", "🍽️ Cenas"])

    with desayuno:
        st.write("- Avena con fruta\n- Yogur natural\n- Tostadas integrales")

    with comida:
        st.write("- Pollo con arroz\n- Lentejas\n- Pasta integral")

    with cena:
        st.write("- Pescado al horno\n- Tortilla\n- Verduras")

# ======================================================
# 💡 HÁBITOS
# ======================================================
elif seccion == "💡 Hábitos saludables":
    st.header("💡 Hábitos saludables")

    st.markdown("""
    - 🏃 Muévete cada día  
    - 💧 Hidratación constante  
    - 😴 Dormir bien  
    - 🧘 Reducir estrés  
    """)

# ----------------------------------
st.caption("NutriGen AI · Proyecto educativo · IA aplicada a la nutrición")
