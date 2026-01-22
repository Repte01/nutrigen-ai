import streamlit as st
from auth.login import login_form, register_form, logout
from services.gemini_client import gemini_chat
from services.chat_service import save_chat, get_chat_history, update_chat_title
from services.pdf_service import generar_pdf_chat
from services.pdf_reader_service import pdf_to_text
from services.pdf_chat_service import save_pdf_chat, get_pdf_chat_history

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

if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = None

if "pdf_name" not in st.session_state:
    st.session_state.pdf_name = None

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
        "📄 Analizar menú PDF",
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
            format="%d",
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

    # -------- HISTORIAL DE CHATS --------
    st.divider()
    st.subheader("🕒 Historial de conversaciones")

    historial = get_chat_history(st.session_state.user.id)

    if not historial:
        st.info("Aún no tienes conversaciones guardadas.")
    else:
        for chat in historial:
            titulo = chat.get("titulo") or "Plan nutricional"

            with st.expander(f"🗂 {titulo} · {chat['created_at']}"):

                nuevo_titulo = st.text_input(
                    "✏️ Renombrar conversación",
                    value=titulo,
                    key=f"titulo_{chat['id']}"
                )

                if nuevo_titulo != titulo:
                    update_chat_title(chat["id"], nuevo_titulo)
                    st.success("✅ Nombre actualizado")
                    st.rerun()

                st.markdown("**🧑 Prompt enviado:**")
                st.code(chat["prompt"])

                st.markdown("**🤖 Respuesta IA:**")
                st.markdown(chat["respuesta"])

                pdf_buffer = generar_pdf_chat(
                    prompt=chat["prompt"],
                    respuesta=chat["respuesta"]
                )

                st.download_button(
                    label="📄 Exportar a PDF",
                    data=pdf_buffer,
                    file_name=f"nutrigen_plan_{chat['created_at']}.pdf",
                    mime="application/pdf"
                )

# ======================================================
# 📄 ANALIZAR MENÚ PDF
# ======================================================
elif seccion == "📄 Analizar menú PDF":
    st.header("📄 Analizar menú nutricional en PDF")
    st.write("Sube un menú en PDF y haz preguntas sobre su contenido.")

    uploaded_pdf = st.file_uploader(
        "📎 Subir menú nutricional (PDF)",
        type=["pdf"]
    )

    if uploaded_pdf:
        st.session_state.pdf_name = uploaded_pdf.name

        if st.session_state.pdf_text is None:
            with st.spinner("📄 Analizando el PDF..."):
                st.session_state.pdf_text = pdf_to_text(uploaded_pdf)

        st.success(f"✅ PDF cargado: {st.session_state.pdf_name}")

        pregunta = st.text_input(
            "❓ Haz una pregunta sobre el menú",
            placeholder="Ej: ¿Hay alimentos con gluten?"
        )

        if st.button("🤖 Preguntar a la IA") and pregunta:
            with st.spinner("🧠 Analizando el menú..."):
                prompt = f"""
Este es un menú nutricional en formato texto:

{st.session_state.pdf_text}

Responde de forma clara y concisa a la siguiente pregunta:
{pregunta}
"""

                respuesta = gemini_chat(prompt)

                save_pdf_chat(
                    user_id=st.session_state.user.id,
                    pdf_name=st.session_state.pdf_name,
                    pregunta=pregunta,
                    respuesta=respuesta
                )

            st.markdown("### 🤖 Respuesta de la IA")
            st.markdown(respuesta)

        st.divider()
        st.subheader("🕒 Historial de preguntas de este PDF")

        historial_pdf = get_pdf_chat_history(
            st.session_state.user.id,
            st.session_state.pdf_name
        )

        if not historial_pdf:
            st.info("Aún no hay preguntas guardadas para este PDF.")
        else:
            for chat in historial_pdf:
                with st.expander(f"❓ {chat['pregunta']}"):
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
