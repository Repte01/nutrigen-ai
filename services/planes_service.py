from services.supabase_client import supabase


def guardar_plan(
    user_id: str,
    objetivo: str,
    nivel_implicacion: int,
    alergias: list,
    restricciones: list,
    prompt: str,
    respuesta: str
):
    data = {
        "user_id": user_id,
        "objetivo": objetivo,
        "nivel_implicacion": nivel_implicacion,
        "alergias": ", ".join(alergias) if alergias else None,
        "restricciones": ", ".join(restricciones) if restricciones else None,
        "prompt": prompt,
        "respuesta_ia": respuesta,
    }

    supabase.table("planes_nutricionales").insert(data).execute()


def obtener_planes_usuario(user_id: str):
    response = (
        supabase
        .table("planes_nutricionales")
        .select("*")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .execute()
    )

    return response.data
