from src.services.pdf_parser import extract_text_from_pdf

def test_extract_text_empty():
    assert extract_text_from_pdf(None) == ""
