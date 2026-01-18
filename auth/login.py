import streamlit as st
import re
from services.supabase_client import supabase


def email_valido(email):
    patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(patron, email)


def password_segura(password):
    return len(password) >= 6


def register_form():
    st.subheader("📝 Registro")

    email = st.text_input("Email")
    password = st.text_input("Contraseña", type="password")
    objetivo = st.text_input("Objetivo nutricional")
    restricciones = st.text_input("Restricciones alimentarias")

    if st.button("Registrarse"):
        if not email_valido(email):
            st.error("Email no válido")
            return

        if not password_segura(password):
            st.error("La contraseña debe tener al menos 6 caracteres")
            return

        try:
            auth_response = supabase.auth.sign_up({
                "email": email,
                "password": password
            })

            user = auth_response.user

            if user is None:
                st.error("No se pudo crear el usuario")
                return

            supabase.table("usuarios").insert({
                "id": user.id,
                "email": email,
                "objetivo": objetivo,
                "restricciones": restricciones
            }).execute()

            st.success("Registro completado. Ahora puedes iniciar sesión.")

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

            user = auth_response.user

            if user:
                st.session_state.logged_in = True
                st.session_state.user = user
                st.experimental_rerun()
            else:
                st.error("Credenciales incorrectas")

        except Exception:
            st.error("Error al iniciar sesión")
