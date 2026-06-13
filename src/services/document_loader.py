from pathlib import Path
from PyPDF2 import PdfReader

class DocumentLoader:
    def load_documents(self, directory):
        documents = []
        path = Path(directory)

        # Load PDF files
        for file in path.glob("*.pdf"):
            reader = PdfReader(file)
            for i, page in enumerate(reader.pages):
                text = page.extract_text()
                if text:
                    documents.append({
                        "filename": file.name,
                        "page": i + 1,  # Human readable page numbering
                        "content": text
                    })

        # Load TXT files
        for file in path.glob("*.txt"):
            with open(file, "r", encoding="utf-8") as f:
                documents.append({
                    "filename": file.name,
                    "page": 1,  # TXT files are usually single page
                    "content": f.read()
                })

        return documents