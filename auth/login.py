import streamlit as st
from services.supabase_client import supabase


# -------------------------
# REGISTRO
# -------------------------
def register_form():
    st.subheader("📝 Registro")

    with st.form("register_form"):
        email = st.text_input("Email")
        password = st.text_input("Contraseña", type="password")
        objetivo = st.text_input("Objetivo nutricional")
        restricciones = st.text_input("Restricciones alimentarias")

        submit = st.form_submit_button("Registrarse")

    if submit:
        if not email or not password:
            st.error("❌ Email y contraseña son obligatorios")
            return

        try:
            # 1️⃣ Crear usuario en Supabase Auth
            auth_response = supabase.auth.sign_up({
                "email": email,
                "password": password
            })

            user = auth_response.user
            session = auth_response.session

            if user is None or session is None:
                st.error("❌ No se pudo crear la sesión del usuario")
                return

            # 2️⃣ Establecer sesión ACTIVA (CLAVE DEL PROBLEMA)
            supabase.auth.set_session(
                session.access_token,
                session.refresh_token
            )

            # 3️⃣ Crear perfil en la tabla usuarios
            supabase.table("usuarios").insert({
                "id": user.id,
                "email": email,
                "objetivo": objetivo,
                "restricciones": restricciones
            }).execute()

            # 4️⃣ Guardar sesión en Streamlit
            st.session_state.user = user
            st.session_state.logged_in = True

            st.success("✅ Registro completado correctamente")
            st.rerun()

        except Exception as e:
            st.error(f"❌ Error en el registro: {e}")


# -------------------------
# LOGIN
# -------------------------
def login_form():
    st.subheader("🔐 Login")

    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Contraseña", type="password")
        submit = st.form_submit_button("Iniciar sesión")

    if submit:
        try:
            auth_response = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })

            user = auth_response.user
            session = auth_response.session

            if user is None or session is None:
                st.error("❌ Credenciales incorrectas")
                return

            # Establecer sesión
            supabase.auth.set_session(
                session.access_token,
                session.refresh_token
            )

            st.session_state.user = user
            st.session_state.logged_in = True

            st.success("✅ Sesión iniciada")
            st.rerun()

        except Exception as e:
            st.error(f"❌ Error al iniciar sesión: {e}")


# -------------------------
# LOGOUT
# -------------------------
def logout():
    supabase.auth.sign_out()
    st.session_state.clear()
    st.rerun()
