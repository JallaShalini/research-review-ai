from src.agents.supervisor_agent import supervisor_node
from src.agents.citation_agent import generate_bibtex_entry
from src.models.paper import Paper

def test_supervisor_node():
    state = {"topic": "AI"}
    updates = supervisor_node(state)
    assert "subtopics" in updates
    assert len(updates["subtopics"]) > 0

def test_generate_bibtex():
    p = Paper(
        title="Test",
        authors=["John Doe"],
        year=2020,
        source="ArXiv",
        paper_id="123"
    )
    bib = generate_bibtex_entry(p)
    assert "@article" in bib
    assert "John Doe" in bib
