from services.supabase_client import supabase


def save_chat(user_id, prompt, respuesta):
    supabase.table("chat_historial").insert({
        "user_id": user_id,
        "prompt": prompt,
        "respuesta": respuesta
    }).execute()


def get_chat_history(user_id):
    return (
        supabase.table("chat_historial")
        .select("*")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .execute()
        .data
    )


def update_chat_title(chat_id, title):
    supabase.table("chat_historial").update(
        {"titulo": title}
    ).eq("id", chat_id).execute()
