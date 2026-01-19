from services.supabase_client import supabase

def save_chat(user_id: str, prompt: str, respuesta: str):
    supabase.table("chat_historial").insert({
        "user_id": user_id,
        "prompt": prompt,
        "respuesta": respuesta
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
