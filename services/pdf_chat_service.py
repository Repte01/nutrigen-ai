from services.supabase_client import supabase


def save_pdf_chat(user_id: str, pdf_name: str, pregunta: str, respuesta: str):
    supabase.table("pdf_chat_historial").insert({
        "user_id": user_id,
        "pdf_name": pdf_name,
        "pregunta": pregunta,
        "respuesta": respuesta
    }).execute()


def get_pdf_chat_history(user_id: str, pdf_name: str):
    response = (
        supabase
        .table("pdf_chat_historial")
        .select("*")
        .eq("user_id", user_id)
        .eq("pdf_name", pdf_name)
        .order("created_at", desc=True)
        .execute()
    )
    return response.data
