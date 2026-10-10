import os
import sys

def validate():
    success = True
    if not os.path.exists("output/literature_review.md"):
        print("MISSING: output/literature_review.md")
        success = False
    if not os.path.exists("output/references.bib"):
        print("MISSING: output/references.bib")
        success = False
        
    if success:
        print("Validation SUCCESS: Output files exist.")
        sys.exit(0)
    else:
        print("Validation FAILED.")
        sys.exit(1)

if __name__ == "__main__":
    validate()
