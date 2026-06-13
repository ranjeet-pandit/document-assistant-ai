"""
Splits documents into chunks.
"""


class TextSplitter:
    def split_text(self, text, chunk_size=600, overlap=100):
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            # Move start forward by chunk_size MINUS the overlap
            start += (chunk_size - overlap)
            
        return chunks