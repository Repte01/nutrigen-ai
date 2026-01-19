import streamlit as st
from auth.login import login_form, register_form, logout
from services.gemini_client import gemini_chat
from services.planes_service import guardar_plan, obtener_planes_usuario

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
user = st.session_state.user
user_id = user.id

st.title("🥗 NutriGen AI")
st.subheader("Tu asistente nutricional inteligente")

st.sidebar.button("🚪 Cerrar sesión", on_click=logout)

st.sidebar.title("📌 Secciones")
seccion = st.sidebar.radio(
    "Ir a:",
    [
        "🥗 Menús saludables",
        "🤖 Asistente IA",
        "📜 Mis planes",
        "💡 Hábitos saludables"
    ]
)

# ======================================================
# 🥗 MENÚS SALUDABLES
# ======================================================
if seccion == "🥗 Menús saludables":
    st.header("🥗 Menús saludables")
    st.info("Ejemplos orientativos para el día a día.")

    desayuno, comida, cena = st.tabs(["🍳 Desayunos", "🍛 Comidas", "🍽️ Cenas"])

    with desayuno:
        st.markdown("""
        - 🥣 Avena con fruta y semillas  
        - 🍞 Tostadas integrales con aguacate  
        - 🥛 Yogur natural con nueces
        """)

    with comida:
        st.markdown("""
        - 🍗 Pollo con arroz y verduras  
        - 🥬 Lentejas con verduras  
        - 🍝 Pasta integral con atún
        """)

    with cena:
        st.markdown("""
        - 🐟 Pescado al horno  
        - 🍳 Tortilla con espinacas  
        - 🥕 Crema de verduras
        """)

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
                "Mejorar salud general"
            ]
        )

        implicacion = st.slider(
            "⚖️ Nivel de implicación",
            1, 3, 2
        )

        alergias = st.multiselect(
            "🚫 Alergias",
            ["Gluten", "Lactosa", "Huevo", "Marisco", "Frutos secos"]
        )

        restricciones = st.multiselect(
            "🥦 Restricciones",
            ["Vegetariano", "Vegano", "Keto", "Sin gluten"]
        )

    with col2:
        observaciones = st.text_area(
            "📝 Observaciones adicionales",
            height=200
        )

    prompt = f"""
Eres un nutricionista profesional.

Objetivo: {objetivo}
Nivel de implicación: {implicacion}/3
Alergias: {', '.join(alergias) if alergias else 'Ninguna'}
Restricciones: {', '.join(restricciones) if restricciones else 'Ninguna'}
Observaciones: {observaciones if observaciones else 'Ninguna'}

Genera un plan claro, práctico y realista.
"""

    st.code(prompt)

    if st.button("✨ Generar plan nutricional"):
        with st.spinner("Generando plan..."):
            respuesta = gemini_chat(prompt)

        guardar_plan(
            user_id,
            objetivo,
            implicacion,
            alergias,
            restricciones,
            prompt,
            respuesta
        )

        st.success("✅ Plan guardado")
        st.markdown(respuesta)

# ======================================================
# 📜 MIS PLANES
# ======================================================
elif seccion == "📜 Mis planes":
    st.header("📜 Mis planes nutricionales")

    planes = obtener_planes_usuario(user_id)

    if not planes:
        st.info("Aún no has generado ningún plan.")
    else:
        for plan in planes:
            with st.expander(f"🗓️ {plan['created_at']} — {plan['objetivo']}"):
                st.markdown(plan["respuesta_ia"])

# ======================================================
# 💡 HÁBITOS SALUDABLES
# ======================================================
elif seccion == "💡 Hábitos saludables":
    st.header("💡 Hábitos saludables")

    st.markdown("""
    - 🏃 Actividad física regular  
    - 💧 Hidratación diaria  
    - 😴 Dormir 7–9 horas  
    - 🧘 Reducir estrés
    """)

# ----------------------------------
st.caption("NutriGen AI · Proyecto educativo")
