from project.documents.models import Document, DocumentChunk, make_chunk_id


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0.")

    if overlap < 0:
        raise ValueError("overlap cannot be negative.")

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size.")

    text = text.strip()

    if not text:
        return []

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start = end - overlap

    return chunks


def chunk_document(
    document: Document,
    chunk_size: int = 500,
    overlap: int = 50,
) -> list[DocumentChunk]:
    text_chunks = chunk_text(
        document.text,
        chunk_size=chunk_size,
        overlap=overlap,
    )

    chunks = []

    for index, text in enumerate(text_chunks):
        chunk = DocumentChunk(
            id=make_chunk_id(document.id, index),
            document_id=document.id,
            chunk_index=index,
            text=text,
            source_path=document.source_path,
            filename=document.filename,
        )
        chunks.append(chunk)

    return chunks