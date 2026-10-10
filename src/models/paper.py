from pydantic import BaseModel, Field
from typing import Optional, List

class Paper(BaseModel):
    title: str
    authors: List[str]
    abstract: Optional[str] = None
    year: Optional[int] = None
    source: str
    paper_id: str
    doi: Optional[str] = None
    pdf_url: Optional[str] = None
    summary: Optional[str] = None
    bibtex: Optional[str] = None
