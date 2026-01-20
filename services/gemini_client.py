import os
from google import genai
from google.genai.errors import ServerError

def gemini_chat(prompt: str) -> str:
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise Exception("❌ GEMINI_API_KEY no encontrada")

    client = genai.Client(api_key=api_key)

    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt
        )

        if not response or not response.text:
            return (
                "⚠️ La IA no ha podido generar una respuesta en este momento.\n\n"
                "Por favor, inténtalo de nuevo en unos segundos."
            )

        return response.text

    except ServerError:
        return (
            "🚧 El servicio de inteligencia artificial está temporalmente saturado.\n\n"
            "👉 Esto NO es un error tuyo.\n"
            "👉 Vuelve a intentarlo en unos segundos."
        )

    except Exception as e:
        return (
            "❌ Se ha producido un error inesperado al generar el plan.\n\n"
            f"Detalle técnico: {str(e)}"
        )
