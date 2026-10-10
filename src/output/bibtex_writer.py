import os
from src.models.workflow_state import WorkflowState
from loguru import logger

def write_bibtex_file(state: dict, output_dir: str = "output"):
    os.makedirs(output_dir, exist_ok=True)
    bibtex_path = os.path.join(output_dir, "references.bib")
    
    references = state.get("references", "")
    
    with open(bibtex_path, "w", encoding="utf-8") as f:
        f.write(references)
        
    logger.info(f"Generated BibTeX file at {bibtex_path}")
