
from src.models.workflow_state import WorkflowState
from src.services.pdf_parser import extract_text_from_pdf
from src.services.ollama_service import generate_summary
from loguru import logger


MAX_PAPERS_TO_SUMMARIZE = 5


def summarization_node(state: WorkflowState) -> dict:
    logger.info("Summarization Agent: Generating summaries for papers")

    papers = state.get("papers", [])
    updated_papers = []
    summaries = []

    for paper in papers[:MAX_PAPERS_TO_SUMMARIZE]:
        logger.info("Summarizing paper: {}", paper.title)

        text = ""
        is_abstract = False

        # Try extracting text from the PDF first.
        if paper.pdf_url:
            try:
                text = extract_text_from_pdf(paper.pdf_url) or ""
            except Exception as exc:
                logger.warning(
                    "PDF extraction failed for '{}': {}",
                    paper.title,
                    exc,
                )

        # Fall back to the abstract if the PDF is unavailable.
        if not text.strip():
            logger.info(
                "Falling back to abstract for '{}'",
                paper.title,
            )
            text = paper.abstract or ""
            is_abstract = True

        if not text.strip():
            summary = (
                "Summary unavailable: no accessible PDF text or abstract."
            )
            logger.warning("No source text available for '{}'", paper.title)
        else:
            try:
                    summary = generate_summary(
                        text,
                        title=paper.title
                    )
            except Exception as exc:
                logger.exception(
                    "Summarization failed for '{}': {}",
                    paper.title,
                    exc,
                )
                summary = (
                    "Summary unavailable because the summarization "
                    "service failed."
                )

        paper.summary = summary
        updated_papers.append(paper)
        summaries.append(summary)

    if len(papers) > MAX_PAPERS_TO_SUMMARIZE:
        logger.info(
            "Summarized {} of {} papers to limit local LLM workload",
            len(updated_papers),
            len(papers),
        )

    return {
        "papers": updated_papers,
        "summaries": summaries,
    }
