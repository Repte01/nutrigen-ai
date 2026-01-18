import streamlit as st
from supabase import create_client, Client

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

# Crear cliente de Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Configuración adicional (opcional)
try:
    # Verificar conexión
    response = supabase.auth.get_session()
    st.log("✅ Conexión a Supabase establecida")
except Exception as e:
    st.error(f"❌ Error conectando a Supabase: {e}")
