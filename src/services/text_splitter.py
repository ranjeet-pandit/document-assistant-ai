"""
Splits documents into chunks.
"""


class TextSplitter:

    def split_text(
        self,
        text,
        chunk_size=150
    ):

        chunks = []

        for i in range(
            0,
            len(text),
            chunk_size
        ):

            chunks.append(
                text[i:i + chunk_size]
            )

        return chunks