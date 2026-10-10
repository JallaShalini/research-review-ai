from src.models.workflow_state import WorkflowState
from src.services.arxiv_service import search_arxiv
from src.services.semantic_scholar_service import search_semantic_scholar
from src.services.crossref_service import search_crossref
from loguru import logger

def web_search_node(state: WorkflowState) -> dict:
    logger.info("Web Search Agent: Starting search across APIs")
    subtopics = state.get("subtopics", [])
    if not subtopics:
        subtopics = [state.get("topic", "")]
        
    all_papers = []
    seen_ids = set()
    
    query = subtopics[0]
    
    arxiv_papers = search_arxiv(query)
    for p in arxiv_papers:
        if p.paper_id and p.paper_id not in seen_ids:
            all_papers.append(p)
            seen_ids.add(p.paper_id)
            
    s2_papers = search_semantic_scholar(query)
    for p in s2_papers:
        if p.paper_id and p.paper_id not in seen_ids:
            all_papers.append(p)
            seen_ids.add(p.paper_id)
            
    crossref_papers = search_crossref(query)
    for p in crossref_papers:
        if p.paper_id and p.paper_id not in seen_ids:
            all_papers.append(p)
            seen_ids.add(p.paper_id)
            
    logger.info(f"Web Search Agent: Found {len(all_papers)} unique papers")
    return {"papers": all_papers}
