# pyrefly: ignore [missing-import]
import arxiv
from loguru import logger
from src.models.paper import Paper
from configs import settings

def search_arxiv(topic: str, max_results: int = 5) -> list[Paper]:
    max_results = getattr(settings, 'MAX_PAPERS', 5)
    logger.info(f"Searching arXiv for: {topic}")
    papers = []
    try:
        client = arxiv.Client()
        search = arxiv.Search(
            query=topic,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance
        )
        
        for result in client.results(search):
            paper = Paper(
                title=result.title,
                authors=[author.name for author in result.authors],
                abstract=result.summary,
                year=result.published.year if result.published else None,
                source="arXiv",
                paper_id=result.get_short_id(),
                pdf_url=result.pdf_url,
                doi=result.doi
            )
            papers.append(paper)
        logger.info(f"Found {len(papers)} papers on arXiv")
    except Exception as e:
        logger.error(f"Error searching arXiv: {e}")
    return papers
