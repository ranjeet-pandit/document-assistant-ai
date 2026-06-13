"""
Splits documents into chunks.
"""

from utils.logger import get_logger

# Initialize the logger named after this specific service file
logger = get_logger("services.text_splitter")

class TextSplitter:
    def split_text(self, text, chunk_size=600, overlap=100):
        logger.info(f"Initializing split: chunk_size={chunk_size}, overlap={overlap}")
        
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start += (chunk_size - overlap)
            
        logger.info(f"Splitting completed successfully. Generated {len(chunks)} chunks.")
        return chunks