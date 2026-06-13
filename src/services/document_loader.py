"""
Loads documents from disk.
"""

from pathlib import Path

from PyPDF2 import PdfReader

class DocumentLoader:

    def load_documents(self, directory):

        documents = []

        path = Path(directory)

        # Load TXT files
        for file in path.glob("*.txt"):

            with open(
                file,
                "r",
                encoding="utf-8"
            ) as f:

                documents.append(
                    {
                        "filename": file.name,
                        "content": f.read()
                    }
                )

        # Load PDF files
        for file in path.glob("*.pdf"):

            reader = PdfReader(file)

            content = ""

            for page in reader.pages:

                text = page.extract_text()

                if text:
                    content += text + "\n"

            documents.append(
                {
                    "filename": file.name,
                    "content": content
                }
            )

        return documents