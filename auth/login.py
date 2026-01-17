import streamlit as st
from services.supabase_client import supabase

def register_form():
    st.subheader("📝 Registro")

    email = st.text_input("Email")
    password = st.text_input("Contraseña", type="password")
    objetivo = st.text_input("Objetivo nutricional")
    restricciones = st.text_input("Restricciones alimentarias")

    if st.button("Registrarse"):
        try:
            # 1. Crear usuario en Supabase Auth (password hasheada automáticamente)
            auth_response = supabase.auth.sign_up({
                "email": email,
                "password": password
            })

            user = auth_response.user

            # 2. Crear perfil en la tabla usuarios
            supabase.table("usuarios").insert({
                "id": user.id,
                "email": email,
                "objetivo": objetivo,
                "restricciones": restricciones
            }).execute()

            st.success("Registro correcto. Ahora puedes iniciar sesión.")

        except Exception as e:
            st.error(f"Error en el registro: {e}")

def login_form():
    st.subheader("🔐 Login")

    email = st.text_input("Email", key="login_email")
    password = st.text_input("Contraseña", type="password", key="login_password")

    if st.button("Iniciar sesión"):
        try:
            auth_response = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })

            st.session_state.logged_in = True
            st.session_state.user = auth_response.user

            st.success("Login correcto")
            st.experimental_rerun()

        except Exception as e:
            st.error("Email o contraseña incorrectos")
