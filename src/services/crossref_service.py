import requests
from loguru import logger
from src.models.paper import Paper
from configs import settings
from src.utils.retry import api_retry
import urllib.parse

@api_retry
def _make_crossref_request(query: str, limit: int):
    query_encoded = urllib.parse.quote(query)
    url = f"https://api.crossref.org/works?query={query_encoded}&rows={limit}&select=DOI,title,author,abstract,issued,link"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()

def search_crossref(topic: str, max_results: int = 5) -> list[Paper]:
    max_results = getattr(settings, 'MAX_PAPERS', 5)
    logger.info(f"Searching Crossref for: {topic}")
    papers = []
    try:
        data = _make_crossref_request(topic, max_results)
        items = data.get("message", {}).get("items", [])
        
        for item in items:
            title = item.get("title", [""])[0] if item.get("title") else ""
            authors = []
            for author in item.get("author", []):
                name = f"{author.get('given', '')} {author.get('family', '')}".strip()
                if name:
                    authors.append(name)
            
            doi = item.get("DOI")
            
            year = None
            if "issued" in item and "date-parts" in item["issued"]:
                parts = item["issued"]["date-parts"]
                if parts and len(parts[0]) > 0:
                    year = parts[0][0]
            
            pdf_url = None
            links = item.get("link", [])
            for link in links:
                if link.get("content-type") == "application/pdf":
                    pdf_url = link.get("URL")
                    break

            paper = Paper(
                title=title,
                authors=authors,
                abstract=item.get("abstract"),
                year=year,
                source="Crossref",
                paper_id=doi if doi else title,
                doi=doi,
                pdf_url=pdf_url
            )
            papers.append(paper)
        logger.info(f"Found {len(papers)} papers on Crossref")
    except Exception as e:
        logger.error(f"Error searching Crossref: {e}")
    return papers
