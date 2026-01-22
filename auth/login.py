import streamlit as st
from services.supabase_client import supabase


def register_form():
    with st.form("register"):
        email = st.text_input("Email")
        password = st.text_input("Contraseña", type="password")
        if st.form_submit_button("Registrarse"):
            supabase.auth.sign_up({"email": email, "password": password})
            st.success("Registro correcto. Revisa tu email.")


def login_form():
    with st.form("login"):
        email = st.text_input("Email")
        password = st.text_input("Contraseña", type="password")
        if st.form_submit_button("Entrar"):
            auth = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            st.session_state.logged_in = True
            st.session_state.user = auth.user
            st.rerun()


def logout():
    supabase.auth.sign_out()
    st.session_state.clear()
    st.rerun()
