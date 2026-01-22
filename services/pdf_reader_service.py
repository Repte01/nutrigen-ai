from PyPDF2 import PdfReader


def pdf_to_text(file):
    reader = PdfReader(file)
    return "\n".join(
        page.extract_text() or "" for page in reader.pages
    ).strip()
