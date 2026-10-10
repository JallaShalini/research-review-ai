import requests
from loguru import logger
from src.models.paper import Paper
from configs import settings
from src.utils.retry import api_retry

@api_retry
def _make_s2_request(query: str, limit: int):
    url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={query}&limit={limit}&fields=title,authors,abstract,year,externalIds,openAccessPdf"
    headers = {}
    if settings.SEMANTIC_SCHOLAR_API_KEY:
        headers["x-api-key"] = settings.SEMANTIC_SCHOLAR_API_KEY
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    return response.json()

def search_semantic_scholar(topic: str, max_results: int = 5) -> list[Paper]:
    max_results = getattr(settings, 'MAX_PAPERS', 5)
    logger.info(f"Searching Semantic Scholar for: {topic}")
    papers = []
    try:
        data = _make_s2_request(topic, max_results)
        
        if "data" in data:
            for item in data["data"]:
                authors = [author.get("name", "") for author in item.get("authors", [])]
                ext_ids = item.get("externalIds", {})
                doi = ext_ids.get("DOI")
                paper_id = item.get("paperId")
                
                pdf_url = None
                oa_pdf = item.get("openAccessPdf")
                if oa_pdf and isinstance(oa_pdf, dict):
                    pdf_url = oa_pdf.get("url")
                
                paper = Paper(
                    title=item.get("title", ""),
                    authors=authors,
                    abstract=item.get("abstract"),
                    year=item.get("year"),
                    source="Semantic Scholar",
                    paper_id=paper_id,
                    doi=doi,
                    pdf_url=pdf_url
                )
                papers.append(paper)
        logger.info(f"Found {len(papers)} papers on Semantic Scholar")
    except Exception as e:
        if "429" in str(e):
            logger.warning("Semantic Scholar rate limited (HTTP 429). Proceeding with remaining configured data sources.")
        else:
            logger.warning(f"Error searching Semantic Scholar: {e}")
    return papers
