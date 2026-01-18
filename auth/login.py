import streamlit as st
from services.supabase_client import supabase
import time

def register_form():
    st.markdown("### 📝 Crear nueva cuenta")
    
    with st.form("register", clear_on_submit=True):
        email = st.text_input("📧 Correo electrónico", placeholder="tu@email.com")
        password = st.text_input("🔑 Contraseña", type="password", 
                                help="Mínimo 6 caracteres")
        confirm_password = st.text_input("🔐 Confirmar contraseña", type="password")
        
        # Términos y condiciones
        accept_terms = st.checkbox("Acepto los términos y condiciones")
        
        submit = st.form_submit_button("🚀 Crear cuenta", use_container_width=True)
    
    if submit:
        if not email or not password:
            st.error("⚠️ Por favor completa todos los campos")
        elif password != confirm_password:
            st.error("⚠️ Las contraseñas no coinciden")
        elif len(password) < 6:
            st.error("⚠️ La contraseña debe tener al menos 6 caracteres")
        elif not accept_terms:
            st.error("⚠️ Debes aceptar los términos y condiciones")
        else:
            try:
                with st.spinner("Creando tu cuenta..."):
                    result = supabase.auth.sign_up({
                        "email": email,
                        "password": password
                    })
                
                if result.user:
                    st.success("🎉 ¡Cuenta creada con éxito!")
                    st.info("📧 Revisa tu correo para confirmar la cuenta")
                    st.balloons()
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error("❌ Error al crear la cuenta")
                    
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")


def login_form():
    st.markdown("### 🔐 Iniciar sesión")
    
    with st.form("login"):
        email = st.text_input("📧 Correo electrónico", placeholder="tu@email.com")
        password = st.text_input("🔑 Contraseña", type="password")
        
        # Recordar sesión
        remember_me = st.checkbox("Recordar sesión")
        
        submit = st.form_submit_button("👉 Ingresar", use_container_width=True)
    
    if submit:
        if not email or not password:
            st.error("⚠️ Por favor ingresa tus credenciales")
        else:
            try:
                with st.spinner("Verificando credenciales..."):
                    res = supabase.auth.sign_in_with_password({
                        "email": email,
                        "password": password
                    })

                if res.user:
                    st.session_state.user = res.user
                    st.session_state.logged = True
                    st.session_state.remember = remember_me
                    
                    st.success(f"✅ ¡Bienvenido/a de nuevo!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Credenciales incorrectas")
                    
            except Exception as e:
                error_msg = str(e)
                if "Invalid login credentials" in error_msg:
                    st.error("❌ Email o contraseña incorrectos")
                elif "Email not confirmed" in error_msg:
                    st.error("⚠️ Por favor confirma tu email primero")
                else:
                    st.error(f"❌ Error: {error_msg}")


def logout():
    try:
        supabase.auth.sign_out()
        st.session_state.clear()
        st.success("✅ Sesión cerrada correctamente")
        time.sleep(1)
        st.rerun()
    except Exception as e:
        st.error(f"❌ Error al cerrar sesión: {e}")
