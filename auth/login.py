import streamlit as st
from services.supabase_client import supabase


def register_form():
    st.subheader("📝 Registro")

    with st.form("register"):
        email = st.text_input("Email")
        password = st.text_input("Contraseña", type="password")
        submit = st.form_submit_button("Registrarse")

    if submit:
        try:
            supabase.auth.sign_up({
                "email": email,
                "password": password
            })
            st.success("✅ Registro correcto. Revisa tu email.")
        except Exception as e:
            st.error(f"❌ Error registro: {e}")


def login_form():
    st.subheader("🔐 Login")

    with st.form("login"):
        email = st.text_input("Email")
        password = st.text_input("Contraseña", type="password")
        submit = st.form_submit_button("Iniciar sesión")

    if submit:
        try:
            auth = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })

            st.session_state.logged_in = True
            st.session_state.user = auth.user

            st.success("✅ Sesión iniciada")
            st.rerun()

        except Exception as e:
            st.error(f"❌ Error login: {e}")


def logout():
    supabase.auth.sign_out()
    st.session_state.clear()
    st.rerun()
