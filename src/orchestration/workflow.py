import uuid
from langgraph.graph import StateGraph, START, END  # pyrefly: ignore [missing-import]
from src.models.workflow_state import WorkflowState
from src.agents.supervisor_agent import supervisor_node
from src.agents.web_search_agent import web_search_node
from src.agents.summarization_agent import summarization_node
from src.agents.citation_agent import citation_node
from src.services.redis_service import update_state, save_state

def create_workflow():
    workflow = StateGraph(WorkflowState)
    
    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("web_search", web_search_node)
    workflow.add_node("summarization", summarization_node)
    workflow.add_node("citation", citation_node)

    workflow.add_edge(START, "supervisor")
    workflow.add_edge("supervisor", "web_search")
    workflow.add_edge("web_search", "summarization")
    workflow.add_edge("summarization", "citation")
    workflow.add_edge("citation", END)

    return workflow.compile()

def run_workflow(topic: str) -> str:
    run_id = str(uuid.uuid4())
    initial_state = {
        "topic": topic,
        "subtopics": [],
        "papers": [],
        "summaries": [],
        "references": "",
        "errors": [],
        "status": "started"
    }
    
    save_state(run_id, initial_state)
    
    app = create_workflow()
    
    for s in app.stream(initial_state):
        node_name = list(s.keys())[0]
        state_updates = s[node_name]
        update_state(run_id, state_updates)
        
    return run_id
