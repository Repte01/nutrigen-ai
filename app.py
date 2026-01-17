import streamlit as st
import re
from auth.login import login_form, register_form
from services.supabase_client import supabase
from services.gemini_client import generar_respuesta, construir_prompt_nutricional

# =========================
# CONFIGURACIÓN GLOBAL
# =========================
st.set_page_config(
    page_title="NutriGen AI",
    page_icon="🥗",
    layout="wide"
)

st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}
</style>
""", unsafe_allow_html=True)

# =========================
# FUNCIONES DE VALIDACIÓN
# =========================
def email_valido(email):
    patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(patron, email)

def password_segura(password):
    return len(password) >= 6

# =========================
# ESTADOS
# =========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "slide_index" not in st.session_state:
    st.session_state.slide_index = 0

# =========================
# HEADER
# =========================
st.title("🥗 NutriGen AI")
st.caption("Planes nutricionales personalizados con Inteligencia Artificial")

# =========================
# USUARIO NO LOGUEADO
# =========================
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        tabs = st.tabs(["🔐 Login", "📝 Registro"])

        with tabs[0]:
            login_form()

        with tabs[1]:
            register_form()

# =========================
# USUARIO LOGUEADO
# =========================
else:
    user = st.session_state.user
    st.success(f"👋 Bienvenido/a {user.email}")

    secciones = st.tabs(["🥗 Plan Nutricional", "💡 Consejos de Salud"])

    # =====================================================
    # PLAN NUTRICIONAL
    # =====================================================
    with secciones[0]:
        st.subheader("📝 Perfil nutricional")

        with st.form("perfil_form"):
            col1, col2 = st.columns(2)

            with col1:
                objetivo = st.text_input("🎯 Objetivo", placeholder="Ej: perder peso")
                restricciones = st.text_input("🚫 Restricciones", placeholder="Ej: vegano")

            with col2:
                alergias = st.text_input("⚠️ Alergias", placeholder="Ej: frutos secos")
                ingredientes = st.text_area("🥕 Ingredientes disponibles")

            observaciones = st.text_area("📝 Observaciones adicionales")

            guardar = st.form_submit_button("💾 Guardar perfil")

        if guardar:
            if not objetivo:
                st.warning("El objetivo es obligatorio")
            else:
                try:
                    supabase.table("usuarios").update({
                        "objetivo": objetivo,
                        "restricciones": restricciones,
                        "ingredientes": ingredientes
                    }).eq("id", user.id).execute()

                    st.success("Perfil guardado correctamente")
                except Exception as e:
                    st.error("❌ Error al guardar el perfil. Inténtalo más tarde.")

        st.divider()

        st.subheader("🤖 Generar plan nutricional")

        if st.button("🥗 Generar mi plan nutricional"):
            try:
                with st.spinner("⏳ Generando tu plan nutricional..."):
                    prompt = construir_prompt_nutricional({
                        "objetivo": objetivo,
                        "restricciones": restricciones,
                        "alergias": alergias,
                        "ingredientes": ingredientes,
                        "observaciones": observaciones
                    })

                    respuesta = generar_respuesta(prompt)
                    st.session_state.plan = respuesta

            except Exception:
                st.error("⚠️ Error al conectar con la IA. Inténtalo más tarde.")

        if "plan" in st.session_state:
            with st.expander("📅 Ver plan nutricional"):
                st.markdown(st.session_state.plan)

    # =====================================================
    # CONSEJOS DE SALUD
    # =====================================================
    with secciones[1]:
        slides = [
            ("🏃 Ejercicio", "Haz al menos 30 min diarios", "#E8F5E9"),
            ("💧 Hidratación", "Bebe 2L de agua al día", "#E3F2FD"),
            ("😴 Sueño", "Duerme 7-9 horas", "#F3E5F5"),
            ("🥗 Alimentación", "Prioriza comida real", "#FFFDE7"),
        ]

        titulo, texto, color = slides[st.session_state.slide_index]

        st.markdown(f"""
        <div style="background:{color};padding:30px;border-radius:15px">
            <h2>{titulo}</h2>
            <p style="font-size:18px">{texto}</p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1,2,1])

        with col1:
            if st.button("⬅️ Anterior") and st.session_state.slide_index > 0:
                st.session_state.slide_index -= 1
                st.experimental_rerun()

        with col3:
            if st.button("Siguiente ➡️") and st.session_state.slide_index < len(slides)-1:
                st.session_state.slide_index += 1
                st.experimental_rerun()

    st.divider()

    if st.button("🚪 Cerrar sesión"):
        st.session_state.clear()
        st.experimental_rerun()
