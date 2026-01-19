import streamlit as st
from auth.login import login_form, register_form, logout
from services.gemini_client import gemini_chat
from services.chat_service import save_chat, get_chat_history
from datetime import datetime

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
# 🥗 MENÚS SALUDABLES
# ======================================================
if seccion == "🥗 Menús saludables":
    st.header("🥗 Menús saludables")
    st.write("Ejemplos de menús equilibrados para el día a día.")

    desayuno, comida, cena = st.tabs(["🍳 Desayunos", "🍛 Comidas", "🍽️ Cenas"])

    with desayuno:
        st.table({
            "Opción": ["Avena con fruta", "Tostadas integrales", "Yogur natural"],
            "Beneficio": [
                "Energía sostenida",
                "Rico en fibra",
                "Salud digestiva"
            ]
        })

    with comida:
        st.table({
            "Plato": [
                "Pollo con arroz y verduras",
                "Lentejas con verduras",
                "Pasta integral con atún"
            ],
            "Aporte principal": [
                "Proteína + carbohidratos",
                "Proteína vegetal",
                "Energía y saciedad"
            ]
        })

    with cena:
        st.table({
            "Cena ligera": [
                "Pescado al horno con ensalada",
                "Tortilla francesa con espinacas",
                "Crema de verduras"
            ],
            "Ideal para": [
                "Recuperación muscular",
                "Cena rápida",
                "Digestión ligera"
            ]
        })

    st.info("💡 Consejo: ajusta las cantidades según tu objetivo y nivel de actividad.")

# ======================================================
# 🤖 ASISTENTE IA
# ======================================================
elif seccion == "🤖 Asistente IA":
    st.header("🤖 Nutricionista con IA")
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
            help="1 = Poco estricto · 3 = Muy estricto"
        )

        alergias = st.multiselect(
            "🚫 Alergias",
            ["Nueces", "Gluten", "Lactosa", "Huevo", "Marisco"]
        )

        restricciones = st.multiselect(
            "🥦 Restricciones alimentarias",
            ["Vegetariano", "Vegano", "Sin gluten", "Sin lactosa", "Keto"]
        )

    with col2:
        observaciones = st.text_area(
            "📝 Información adicional",
            placeholder="Ej: entreno 4 días por semana, poco tiempo para cocinar...",
            height=180
        )

    prompt = f"""
Eres un nutricionista profesional.

Genera un plan nutricional claro y práctico.

Objetivo: {objetivo}
Nivel de implicación: {implicacion}/3
Alergias: {', '.join(alergias) if alergias else 'Ninguna'}
Restricciones: {', '.join(restricciones) if restricciones else 'Ninguna'}
Observaciones adicionales: {observaciones if observaciones else 'Ninguna'}

Incluye:
- Menú orientativo
- Calorías aproximadas
- Consejos prácticos
"""

    st.markdown("### 📄 Prompt generado automáticamente")
    st.code(prompt)

    if st.button("✨ Generar plan nutricional con IA"):
        with st.spinner("🧠 Pensando como un nutricionista..."):
            respuesta = gemini_chat(prompt)

            save_chat(
                user_id=st.session_state.user.id,
                prompt=prompt,
                respuesta=respuesta
            )

        st.success("✅ Plan generado")
        st.markdown(respuesta)

    # -------- HISTORIAL --------
    st.divider()
    st.subheader("🕒 Historial de conversaciones")

    historial = get_chat_history(st.session_state.user.id)

    if not historial:
        st.info("Aún no tienes conversaciones guardadas.")
    else:
        for chat in historial:
            fecha = datetime.fromisoformat(chat["created_at"]).strftime("%d/%m/%Y %H:%M")
            titulo = chat.get("title") or f"Conversación del {fecha}"

            with st.expander(f"💬 {titulo}"):
                st.caption(f"🗓 {fecha}")
                st.markdown("**🧑 Prompt enviado:**")
                st.code(chat["prompt"])
                st.markdown("**🤖 Respuesta IA:**")
                st.markdown(chat["respuesta"])

# ======================================================
# 💡 HÁBITOS SALUDABLES
# ======================================================
elif seccion == "💡 Hábitos saludables":
    st.header("💡 Hábitos saludables")
    st.write("Pequeñas acciones diarias que mejoran tu salud.")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("🏃 Actividad física")
        st.markdown("""
        - Caminar 30 min diarios  
        - Entrenar fuerza 2-3 veces/semana  
        - Estiramientos
        """)

    with col2:
        st.subheader("💧 Hidratación")
        st.markdown("""
        - 1.5–2L de agua al día  
        - Evitar refrescos  
        - Agua antes de las comidas
        """)

    with col3:
        st.subheader("😴 Descanso")
        st.markdown("""
        - Dormir 7–9 horas  
        - Rutina de sueño  
        - Evitar pantallas antes de dormir
        """)

    st.success("🌱 La constancia vale más que la perfección.")

# ----------------------------------
st.caption("NutriGen AI · Proyecto educativo · IA aplicada a la nutrición")
