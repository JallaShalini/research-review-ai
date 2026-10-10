from src.models.workflow_state import WorkflowState
from loguru import logger

def supervisor_node(state: WorkflowState) -> dict:
    logger.info("Supervisor Agent: Planning workflow")
    topic = state.get("topic", "")
    
    subtopics = [
        f"{topic}",
    ]
    
    logger.info(f"Supervisor Agent generated subtopics: {subtopics}")
    return {"subtopics": subtopics}
