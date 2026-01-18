import streamlit as st
from services.supabase_client import supabase


def register_form():
    st.subheader("📝 Registro")

    with st.form("register"):
        email = st.text_input("Email")
        password = st.text_input("Contraseña", type="password")
        submit = st.form_submit_button("Registrarse")

    if submit:
        supabase.auth.sign_up({
            "email": email,
            "password": password
        })
        st.success("Cuenta creada. Confirma el email.")


def login_form():
    st.subheader("🔐 Login")

    with st.form("login"):
        email = st.text_input("Email")
        password = st.text_input("Contraseña", type="password")
        submit = st.form_submit_button("Iniciar sesión")

    if submit:
        res = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

        st.session_state.user = res.user
        st.session_state.logged = True
        st.rerun()


def logout():
    supabase.auth.sign_out()
    st.session_state.clear()
    st.rerun()
