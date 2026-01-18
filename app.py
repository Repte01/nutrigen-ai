import streamlit as st
from auth.login import login_form, register_form
from services.supabase_client import supabase
from services.gemini_client import generar_respuesta, construir_prompt_nutricional

st.set_page_config(
    page_title="NutriGen AI",
    page_icon="🥗",
    layout="wide"
)

st.title("🥗 NutriGen AI")
st.caption("Planes nutricionales personalizados con Inteligencia Artificial")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "slide_index" not in st.session_state:
    st.session_state.slide_index = 0

if not st.session_state.logged_in:
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Registro"])

    with tab1:
        login_form()

    with tab2:
        register_form()

else:
    user = st.session_state.user
    st.success(f"Bienvenido/a {user.email}")

    tabs = st.tabs(["🥗 Plan Nutricional", "💡 Consejos de Salud"])

    with tabs[0]:
        st.subheader("📝 Perfil nutricional")

        with st.form("perfil"):
            objetivo = st.text_input("Objetivo")
            restricciones = st.text_input("Restricciones")
            alergias = st.text_input("Alergias")
            ingredientes = st.text_area("Ingredientes disponibles")
            observaciones = st.text_area("Observaciones")

            guardar = st.form_submit_button("Guardar perfil")

        if guardar:
            supabase.table("usuarios").update({
                "objetivo": objetivo,
                "restricciones": restricciones
            }).eq("id", user.id).execute()
            st.success("Perfil guardado")

        if st.button("🥗 Generar mi plan nutricional"):
            with st.spinner("Generando plan nutricional..."):
                prompt = construir_prompt_nutricional({
                    "objetivo": objetivo,
                    "restricciones": restricciones,
                    "alergias": alergias,
                    "ingredientes": ingredientes,
                    "observaciones": observaciones
                })
                st.session_state.plan = generar_respuesta(prompt)

        if "plan" in st.session_state:
            st.markdown(st.session_state.plan)

    with tabs[1]:
        slides = [
            ("🏃 Ejercicio", "30 minutos diarios"),
            ("💧 Hidratación", "Bebe 2L de agua"),
            ("😴 Sueño", "Duerme 7-9 horas"),
            ("🥗 Alimentación", "Prioriza comida real")
        ]

        titulo, texto = slides[st.session_state.slide_index]
        st.subheader(titulo)
        st.write(texto)

        col1, col2 = st.columns(2)

        with col1:
            if st.button("⬅️ Anterior") and st.session_state.slide_index > 0:
                st.session_state.slide_index -= 1
                st.experimental_rerun()

        with col2:
            if st.button("Siguiente ➡️") and st.session_state.slide_index < len(slides) - 1:
                st.session_state.slide_index += 1
                st.experimental_rerun()

    if st.button("🚪 Cerrar sesión"):
        st.session_state.clear()
        st.experimental_rerun()
