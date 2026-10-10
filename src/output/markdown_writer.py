import os
from src.models.workflow_state import WorkflowState
from loguru import logger

def write_markdown_report(state: dict, output_dir: str = "output"):
    os.makedirs(output_dir, exist_ok=True)
    report_path = os.path.join(output_dir, "literature_review.md")
    
    topic = state.get("topic", "Unknown Topic")
    papers = state.get("papers", [])
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"# Literature Review: {topic}\n\n")
        f.write("## Introduction\n\n")
        f.write(f"This literature review provides an overview of recent research on {topic}. "
                "The following sections summarize key contributions, methodologies, and findings from selected academic papers.\n\n")
        
        f.write("## Related Work\n\n")
        for idx, paper in enumerate(papers, 1):
            title = paper.title or "Untitled Document"
            f.write(f"### {title}\n\n")
            summary = paper.summary if paper.summary else "No summary available."
            f.write(f"{summary}\n\n")
            
        f.write("## Conclusion\n\n")
        f.write("In conclusion, the reviewed papers offer diverse approaches and significant advancements in the field. "
                "Future research may build upon these methodologies to explore remaining challenges.\n\n")
        
        f.write("## References\n\n")
        for idx, paper in enumerate(papers, 1):
            authors = ", ".join(paper.authors) if paper.authors else "Unknown Authors"
            year = paper.year if paper.year else "n.d."
            title = paper.title or "Untitled Document"
            f.write(f"[{idx}] {authors} ({year}). {title}.\n")
            
    logger.info(f"Generated Markdown report at {report_path}")
