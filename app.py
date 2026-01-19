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
    st.write("Ideas prácticas y equilibradas para organizar tus comidas.")

    objetivo_menu = st.selectbox(
        "🎯 Filtrar según objetivo",
        ["General", "Pérdida de grasa", "Ganancia muscular", "Salud general"]
    )

    st.subheader("📅 Ejemplo de menú diario")

    st.markdown("""
**🥣 Desayuno**
- Avena con fruta y semillas  
- Café o té sin azúcar  

**🍎 Media mañana**
- Yogur natural + frutos secos  

**🍛 Comida**
- Pollo a la plancha  
- Arroz integral  
- Verduras salteadas  

**🥪 Merienda**
- Tostada integral con aguacate  

**🍽️ Cena**
- Pescado al horno  
- Ensalada verde
""")

    st.divider()
    st.subheader("🍽️ Tipos de menú")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 🟢 Menú ligero")
        st.write("Ideal para cenas o días de descanso.")
        st.markdown("""
- Cremas de verduras  
- Pescado blanco  
- Yogur natural  
""")

    with col2:
        st.markdown("### 🔵 Menú equilibrado")
        st.write("Perfecto para el día a día.")
        st.markdown("""
- Proteína + carbohidrato  
- Verduras  
- Grasas saludables  
""")

    with col3:
        st.markdown("### 🔴 Menú alto en proteína")
        st.write("Enfocado a ganancia muscular.")
        st.markdown("""
- Carnes magras  
- Legumbres  
- Huevos / tofu  
""")

    st.info("""
💡 **Consejos prácticos**
- Ajusta cantidades, no alimentos  
- Prioriza comida real  
- La constancia es más importante que la perfección  
""")

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
            titulo = chat.get("titulo") or "Plan nutricional"

            with st.expander(f"🗂 {titulo} · {chat['created_at']}"):
                st.markdown("**🧑 Prompt:**")
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
    st.write("Pequeñas acciones diarias que generan grandes cambios.")

    st.subheader("🌱 Hábitos clave")

    st.markdown("""
### 🍽️ Alimentación
- Come despacio  
- Evita pantallas al comer  
- Prioriza saciedad  

### 🏃 Movimiento
- 8.000–10.000 pasos diarios  
- Fuerza 2–3 veces/semana  
- Muévete aunque no entrenes  

### 😴 Descanso
- Dormir 7–9 horas  
- Rutina estable  
- Cena ligera  

### 🧠 Salud mental
- Respiración consciente  
- Menos estrés  
- Constancia > perfección  
""")

    st.divider()
    st.subheader("✅ Checklist diario")

    agua = st.checkbox("💧 He bebido suficiente agua")
    movimiento = st.checkbox("🏃 Me he movido al menos 30 minutos")
    descanso = st.checkbox("😴 He dormido bien")
    comida = st.checkbox("🥗 He comido consciente")

    if agua and movimiento and descanso and comida:
        st.success("🔥 Día saludable completado. ¡Buen trabajo!")

    st.markdown("> 🌟 *No busques hacerlo perfecto, busca hacerlo sostenible.*")

# ----------------------------------
st.caption("NutriGen AI · Proyecto educativo · IA aplicada a la nutrición")
