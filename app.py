import streamlit as st
from services.gemini_client import gemini_chat

# -----------------------------
# Configuración general
# -----------------------------
st.set_page_config(
    page_title="NutriGen AI",
    page_icon="🥗",
    layout="wide"
)

# -----------------------------
# Cabecera
# -----------------------------
st.title("🥗 NutriGen AI")
st.subheader("Tu asistente nutricional inteligente")

st.markdown(
    """
    Bienvenido/a a **NutriGen AI**, una aplicación que te ayuda a:
    - Crear **menús saludables**
    - Mejorar tus **hábitos de salud**
    - Generar **planes nutricionales personalizados con IA**
    """
)

st.divider()

# -----------------------------
# Navegación lateral
# -----------------------------
st.sidebar.title("📌 Secciones")

seccion = st.sidebar.radio(
    "Ir a:",
    [
        "🥗 Menús saludables",
        "🤖 Asistente IA",
        "💡 Hábitos saludables"
    ]
)

# =========================================================
# 🥗 MENÚS SALUDABLES
# =========================================================
if seccion == "🥗 Menús saludables":
    st.header("🥗 Menús saludables generales")

    st.markdown(
        """
        Ejemplos de menús equilibrados y recomendados para una dieta saludable.
        """
    )

    st.table({
        "Comida": ["Desayuno", "Comida", "Cena"],
        "Ejemplo": [
            "Avena con fruta y yogur",
            "Pollo a la plancha con arroz y verduras",
            "Pescado al horno con ensalada"
        ]
    })

    st.info(
        "💡 Estos menús son orientativos y sirven como base para una alimentación equilibrada."
    )

# =========================================================
# 🤖 ASISTENTE IA
# =========================================================
elif seccion == "🤖 Asistente IA":
    st.header("🤖 Nutricionista con IA")

    st.markdown(
        """
        Describe tus **objetivos**, **alergias**, **restricciones** y preferencias.
        
        **Ejemplo**:  
        *Quiero ganar músculo, soy celíaco y alérgico a las nueces.*
        """
    )

    prompt = st.text_area(
        "📝 Tu solicitud",
        height=150,
        placeholder="Quiero ganar músculo, soy celíaco y alérgico a las nueces"
    )

    if st.button("✨ Generar plan nutricional"):
        if prompt.strip() == "":
            st.warning("⚠️ Escribe una descripción primero")
        else:
            with st.spinner("🧠 Generando plan con IA..."):
                respuesta = gemini_chat(prompt)

            st.success("✅ Plan generado")
            st.markdown(respuesta)

# =========================================================
# 💡 HÁBITOS SALUDABLES
# =========================================================
elif seccion == "💡 Hábitos saludables":
    st.header("💡 Hábitos saludables")

    st.markdown(
        """
        Algunos hábitos clave para mejorar tu salud general:
        """
    )

    st.markdown(
        """
        - 🏃‍♂️ **Actividad física regular** (caminar, correr, gimnasio)
        - 💧 **Buena hidratación** (1.5–2L de agua al día)
        - 😴 **Dormir bien** (7–9 horas)
        - 🥦 **Alimentación equilibrada**
        - 🧘 **Reducir el estrés**
        """
    )

    st.success(
        "🌱 Pequeños cambios diarios generan grandes mejoras a largo plazo."
    )

# -----------------------------
# Footer
# -----------------------------
st.divider()
st.caption("NutriGen AI · Proyecto educativo · IA aplicada a la nutrición")
