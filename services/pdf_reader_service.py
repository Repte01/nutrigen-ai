from PyPDF2 import PdfReader


def pdf_to_text(uploaded_file) -> str:
    """
    Convierte un archivo PDF subido en Streamlit a texto plano.
    """
    reader = PdfReader(uploaded_file)
    texto = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            texto += page_text + "\n"

    return texto.strip()
