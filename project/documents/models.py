from datetime import datetime
from pathlib import Path
from pydantic import BaseModel, Field


class Document(BaseModel):
    id: str = Field(description="Unique document identifier.")
    source_path: str = Field(description="Original file path.")
    filename: str = Field(description="Original file name.")
    extension: str = Field(description="File extension.")
    text: str = Field(description="Full extracted text.")
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())


class DocumentChunk(BaseModel):
    id: str = Field(description="Unique chunk identifier.")
    document_id: str = Field(description="Parent document ID.")
    chunk_index: int = Field(description="Chunk position inside the document.")
    text: str = Field(description="Chunk text.")
    source_path: str = Field(description="Original document path.")
    filename: str = Field(description="Original document filename.")


def make_document_id(path: str | Path) -> str:
    path = Path(path)
    return path.stem.lower().replace(" ", "_")


def make_chunk_id(document_id: str, chunk_index: int) -> str:
    return f"{document_id}_chunk_{chunk_index}"