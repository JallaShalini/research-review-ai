from src.models.workflow_state import WorkflowState
from loguru import logger

def generate_bibtex_entry(paper) -> str:
    year = paper.year if paper.year else "2024"
    authors_str = " and ".join(paper.authors) if paper.authors else "Unknown Authors"
    key_author = paper.authors[0].split()[-1] if paper.authors else "unknown"
    key = f"{key_author}{year}{paper.title.split()[0] if paper.title else 'paper'}".lower()
    
    key = "".join(c for c in key if c.isalnum())
    
    bibtex = f"@article{{{key},\n"
    bibtex += f"  title={{{paper.title}}},\n"
    bibtex += f"  author={{{authors_str}}},\n"
    bibtex += f"  year={{{year}}}\n"
    if paper.doi:
        bibtex += f"  ,doi={{{paper.doi}}}\n"
    bibtex += "}\n"
    return bibtex

def citation_node(state: WorkflowState) -> dict:
    logger.info("Citation Agent: Generating BibTeX citations")
    papers = state.get("papers", [])
    
    references = ""
    updated_papers = []
    
    for paper in papers:
        bib = generate_bibtex_entry(paper)
        paper.bibtex = bib
        references += bib + "\n"
        updated_papers.append(paper)
        
    logger.info("Citation Agent: Finished generating references")
    return {"papers": updated_papers, "references": references, "status": "completed"}
