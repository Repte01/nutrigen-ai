from supabase import create_client
from dotenv import load_dotenv
import os

# Cargar variables del .env
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")

# Crear el cliente de Supabase
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
