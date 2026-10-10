import os

files = [
    "configs/__init__.py",
    "src/__init__.py",
    "src/agents/__init__.py",
    "src/models/__init__.py",
    "src/orchestration/__init__.py",
    "src/output/__init__.py",
    "src/utils/__init__.py",
    "tests/__init__.py",
    "src/orchestration/workflow.py",
    "src/services/arxiv_service.py"
]

for f in files:
    if os.path.exists(f):
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
        if '# pyrefly: ignore [missing-import]' not in content:
            with open(f, 'w', encoding='utf-8') as file:
                file.write('# pyrefly: ignore [missing-import]\n' + content)
