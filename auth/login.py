import streamlit as st
from services.supabase_client import supabase


# -------------------------
# REGISTRO (SIN SESIÓN)
# -------------------------
def register_form():
    st.subheader("📝 Registro")

    with st.form("register_form"):
        email = st.text_input("Email")
        password = st.text_input("Contraseña", type="password")

        submit = st.form_submit_button("Registrarse")

    if submit:
        if not email or not password:
            st.error("❌ Email y contraseña obligatorios")
            return

        try:
            supabase.auth.sign_up({
                "email": email,
                "password": password
            })

            st.success(
                "✅ Registro completado. "
                "Revisa tu email y confirma la cuenta antes de iniciar sesión."
            )

        except Exception as e:
            st.error(f"❌ Error en el registro: {e}")


# -------------------------
# LOGIN (CREA PERFIL SI NO EXISTE)
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
                st.error("❌ Credenciales incorrectas o email no confirmado")
                return

            # Establecer sesión
            supabase.auth.set_session(
                session.access_token,
                session.refresh_token
            )

            # 🔎 Comprobar si existe perfil
            profile = supabase.table("usuarios") \
                .select("id") \
                .eq("id", user.id) \
                .execute()

            if not profile.data:
                # Crear perfil solo la primera vez
                supabase.table("usuarios").insert({
                    "id": user.id,
                    "email": user.email
                }).execute()

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
