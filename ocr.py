import pytesseract
from PIL import Image

# Tesseract location
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def extract_text_from_image(image):
    """
    Extract text from an image using Tesseract OCR.
    """
    try:
        text = pytesseract.image_to_string(image)
        return text.strip()

    except Exception as e:
        return f"OCR Error: {str(e)}"