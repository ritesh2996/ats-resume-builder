from io import BytesIO
from xhtml2pdf import pisa

def html_to_pdf(source_html: str) -> bytes:
    """
    Render HTML string to PDF bytes using xhtml2pdf (pure Python).
    Note: CSS support is limited vs. wkhtmltopdf, but good enough for a clean resume.
    """
    result = BytesIO()
    pisa_status = pisa.CreatePDF(src=source_html, dest=result, encoding="utf-8")
    if pisa_status.err:
        # Return whatever was generated; caller can decide how to handle errors.
        return result.getvalue()
    return result.getvalue()
