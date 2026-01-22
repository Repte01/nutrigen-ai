from services.supabase_client import supabase


def save_pdf_chat(user_id, pdf_name, pregunta, respuesta):
    supabase.table("pdf_chat_historial").insert({
        "user_id": user_id,
        "pdf_name": pdf_name,
        "pregunta": pregunta,
        "respuesta": respuesta
    }).execute()


def get_pdf_chat_history(user_id, pdf_name):
    return (
        supabase.table("pdf_chat_historial")
        .select("*")
        .eq("user_id", user_id)
        .eq("pdf_name", pdf_name)
        .order("created_at", desc=True)
        .execute()
        .data
    )
