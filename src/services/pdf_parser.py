import fitz  # PyMuPDF
import requests
from loguru import logger
import tempfile
import os

def extract_text_from_pdf(pdf_url: str, max_pages: int = 2) -> str:
    if not pdf_url:
        return ""
    
    try:
        response = requests.get(pdf_url, stream=True, timeout=15)
        response.raise_for_status()
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            for chunk in response.iter_content(chunk_size=8192):
                tmp_file.write(chunk)
            tmp_path = tmp_file.name

        text = ""
        try:
            doc = fitz.open(tmp_path)
            for page_num in range(min(max_pages, len(doc))):
                text += doc[page_num].get_text() + "\n"
            doc.close()
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
        
        return text.strip()
    except Exception as e:
        logger.warning(f"Failed to fetch or parse PDF from {pdf_url}: {e}")
        return ""
