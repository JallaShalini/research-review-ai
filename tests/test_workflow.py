from src.orchestration.workflow import create_workflow

def test_create_workflow():
    wf = create_workflow()
    assert wf is not None
