import json
from pathlib import Path

from project.documents.models import Document, DocumentChunk


class DocumentRepository:
    def __init__(self, data_dir: str | Path = "data"):
        self.data_dir = Path(data_dir)
        self.documents_path = self.data_dir / "documents.json"
        self.chunks_path = self.data_dir / "chunks.json"

        self.data_dir.mkdir(parents=True, exist_ok=True)

    def save_document(self, document: Document) -> None:
        documents = self.load_documents()
        documents = [item for item in documents if item.id != document.id]
        documents.append(document)

        self.documents_path.write_text(
            json.dumps([item.model_dump() for item in documents], indent=2),
            encoding="utf-8",
        )

    def save_chunks(self, chunks: list[DocumentChunk]) -> None:
        existing_chunks = self.load_chunks()

        new_chunk_ids = {chunk.id for chunk in chunks}
        existing_chunks = [
            chunk for chunk in existing_chunks if chunk.id not in new_chunk_ids
        ]

        all_chunks = existing_chunks + chunks

        self.chunks_path.write_text(
            json.dumps([chunk.model_dump() for chunk in all_chunks], indent=2),
            encoding="utf-8",
        )

    def load_documents(self) -> list[Document]:
        if not self.documents_path.exists():
            return []

        data = json.loads(self.documents_path.read_text(encoding="utf-8"))
        return [Document(**item) for item in data]

    def load_chunks(self) -> list[DocumentChunk]:
        if not self.chunks_path.exists():
            return []

        data = json.loads(self.chunks_path.read_text(encoding="utf-8"))
        return [DocumentChunk(**item) for item in data]

    def clear(self) -> None:
        self.documents_path.write_text("[]", encoding="utf-8")
        self.chunks_path.write_text("[]", encoding="utf-8")