import fitz
from PIL import Image
import io

from .ocr import extract_text_from_image


def extract_text_from_pdf(file):
    """
    Extract text from PDF.
    If normal text extraction fails, use OCR.
    """

    document = fitz.open(stream=file.read(), filetype="pdf")

    extracted_text = ""

    for page in document:

        # Try normal PDF text extraction
        text = page.get_text()

        if text.strip():
            extracted_text += text + "\n"

        else:
            # Scanned PDF → OCR
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))

            image_bytes = pix.tobytes("png")
            image = Image.open(io.BytesIO(image_bytes))

            ocr_text = extract_text_from_image(image)

            extracted_text += ocr_text + "\n"

    document.close()

    return extracted_text.strip()