from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4


def generar_pdf_chat(prompt: str, respuesta: str) -> BytesIO:
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("<b>NutriGen AI</b>", styles["Title"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>Prompt enviado:</b>", styles["Heading2"]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(prompt.replace("\n", "<br />"), styles["Normal"]))

    story.append(Spacer(1, 20))

    story.append(Paragraph("<b>Respuesta del nutricionista IA:</b>", styles["Heading2"]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(respuesta.replace("\n", "<br />"), styles["Normal"]))

    doc.build(story)
    buffer.seek(0)

    return buffer
