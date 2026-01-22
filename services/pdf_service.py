from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4


def generar_pdf_chat(prompt, respuesta):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()

    doc.build([
        Paragraph("<b>Prompt</b>", styles["Heading2"]),
        Paragraph(prompt.replace("\n", "<br/>"), styles["Normal"]),
        Paragraph("<br/><b>Respuesta</b>", styles["Heading2"]),
        Paragraph(respuesta.replace("\n", "<br/>"), styles["Normal"]),
    ])

    buffer.seek(0)
    return buffer
