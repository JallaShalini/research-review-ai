from typing import TypedDict, List
from src.models.paper import Paper

class WorkflowState(TypedDict):
    topic: str
    subtopics: List[str]
    papers: List[Paper]
    summaries: List[str]
    references: str
    errors: List[str]
    status: str
