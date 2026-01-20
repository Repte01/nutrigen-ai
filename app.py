import streamlit as st
from auth.login import login_form, register_form, logout
from services.gemini_client import gemini_chat
from services.chat_service import save_chat, get_chat_history, update_chat_title
from services.pdf_service import generar_pdf_chat

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
    st.write(
        "Ejemplos de menús equilibrados, fáciles de preparar y adaptables "
        "a diferentes objetivos nutricionales."
    )

    st.divider()

    col1, col2, col3 = st.columns(3)
    col1.metric("🔥 Calorías diarias", "1.800 – 2.200 kcal")
    col2.metric("🥩 Proteínas", "20–30%")
    col3.metric("🥦 Verduras", "En cada comida")

    st.divider()

    desayuno, comida, cena = st.tabs(["🍳 Desayunos", "🍛 Comidas", "🍽️ Cenas"])

    with desayuno:
        st.subheader("🍳 Desayunos equilibrados")
        st.table({
            "Opción": [
                "Avena con fruta y semillas",
                "Tostadas integrales con aguacate",
                "Yogur natural con frutos rojos",
                "Huevos revueltos con verduras"
            ],
            "Beneficio": [
                "Energía sostenida",
                "Grasas saludables",
                "Salud digestiva",
                "Alta saciedad"
            ]
        })

        st.info("💡 Consejo: prioriza proteína por la mañana para controlar el apetito.")

    with comida:
        st.subheader("🍛 Comidas principales")
        st.table({
            "Plato": [
                "Pollo con arroz integral y verduras",
                "Lentejas con verduras",
                "Pasta integral con atún",
                "Quinoa con salmón"
            ],
            "Aporte principal": [
                "Proteína + carbohidratos",
                "Proteína vegetal",
                "Energía y saciedad",
                "Omega 3 y proteína"
            ]
        })

        with st.expander("📌 Ideas rápidas para llevar"):
            st.markdown("""
            - Ensalada de garbanzos con huevo duro  
            - Arroz integral con pollo al horno  
            - Wrap integral de pavo y verduras  
            """)

    with cena:
        st.subheader("🍽️ Cenas ligeras")
        st.table({
            "Cena": [
                "Pescado al horno con ensalada",
                "Tortilla francesa con espinacas",
                "Crema de verduras",
                "Requesón con frutos secos"
            ],
            "Ideal para": [
                "Recuperación muscular",
                "Cena rápida",
                "Digestión ligera",
                "Proteína nocturna"
            ]
        })

        st.warning("⚠️ Evita cenas muy copiosas o ricas en azúcares simples.")

    st.success("✅ Un buen menú no es perfecto, es sostenible.")

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
# 💡 HÁBITOS SALUDABLES
# ======================================================
elif seccion == "💡 Hábitos saludables":
    st.header("💡 Hábitos saludables")
    st.write(
        "Pequeñas acciones diarias que, mantenidas en el tiempo, "
        "marcan una gran diferencia en tu salud."
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("🏃 Actividad física")
        st.markdown("""
        - Caminar 8.000–10.000 pasos/día  
        - Fuerza 2–3 veces/semana  
        - Cardio moderado  
        - Movilidad y estiramientos
        """)

    with col2:
        st.subheader("💧 Hidratación y nutrición")
        st.markdown("""
        - 1.5–2L de agua diarios  
        - Priorizar comida real  
        - Fruta y verdura diaria  
        - Evitar ultraprocesados
        """)

    with col3:
        st.subheader("😴 Descanso y mente")
        st.markdown("""
        - Dormir 7–9 horas  
        - Rutina de sueño estable  
        - Menos pantallas de noche  
        - Gestión del estrés
        """)

    with st.expander("📆 Rutina saludable semanal"):
        st.markdown("""
        **Lunes–Viernes**
        - Movimiento diario  
        - Comidas regulares  
        - Hidratación constante  

        **Fin de semana**
        - Descanso activo  
        - Flexibilidad sin culpa  
        """)

    st.success("🌱 La constancia vale más que la perfección.")

# ----------------------------------
st.caption("NutriGen AI · Proyecto educativo · IA aplicada a la nutrición")
