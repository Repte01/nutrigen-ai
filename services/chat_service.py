from services.supabase_client import supabase


def save_chat(user_id: str, prompt: str, respuesta: str):
    contenido = f"""USUARIO:
{prompt}

IA:
{respuesta}
"""
    supabase.table("chat_historial").insert({
        "user_id": user_id,
        "prompt": prompt,
        "respuesta": contenido
    }).execute()


def get_chat_history(user_id: str):
    response = (
        supabase
        .table("chat_historial")
        .select("*")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .execute()
    )
    return response.data


def update_chat_title(chat_id: str, new_title: str):
    supabase.table("chat_historial").update({
        "titulo": new_title
    }).eq("id", chat_id).execute()


def append_to_chat(chat_id: str, current_text: str, user_msg: str, ia_msg: str):
    nuevo_contenido = f"""{current_text}

USUARIO:
{user_msg}

IA:
{ia_msg}
"""
    supabase.table("chat_historial").update({
        "respuesta": nuevo_contenido
    }).eq("id", chat_id).execute()
