# backend/utils/text_extractor.py
from io import BytesIO
import docx
from PyPDF2 import PdfReader
import chardet

def extract_text_from_bytes(content: bytes, filename: str = "") -> str:
    """
    Try PDF -> DOCX -> plain text. Return extracted text (may be empty).
    """
    lower = filename.lower()
    # PDF
    if lower.endswith(".pdf"):
        try:
            reader = PdfReader(BytesIO(content))
            texts = []
            for p in reader.pages:
                try:
                    texts.append(p.extract_text() or "")
                except Exception:
                    continue
            return "\n".join(texts)
        except Exception:
            return ""

    # DOCX
    if lower.endswith(".docx"):
        try:
            doc = docx.Document(BytesIO(content))
            texts = []
            for para in doc.paragraphs:
                if para.text:
                    texts.append(para.text)
            return "\n".join(texts)
        except Exception:
            return ""

    # try as plain text - detect encoding
    try:
        enc = chardet.detect(content)
        text = content.decode(enc["encoding"] or "utf-8", errors="ignore")
        return text
    except Exception:
        return ""
