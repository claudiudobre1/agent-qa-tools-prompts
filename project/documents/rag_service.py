import re
from collections import Counter

from project.documents.models import DocumentChunk
from project.documents.repository import DocumentRepository


def tokenize(text: str) -> list[str]:
    return re.findall(r"\b\w+\b", text.lower())


def score_chunk(query: str, chunk: DocumentChunk) -> int:
    query_tokens = tokenize(query)
    chunk_tokens = tokenize(chunk.text)

    if not query_tokens or not chunk_tokens:
        return 0

    chunk_counts = Counter(chunk_tokens)

    score = 0
    for token in query_tokens:
        score += chunk_counts.get(token, 0)

    return score


class RAGService:
    def __init__(self, repository: DocumentRepository | None = None):
        self.repository = repository or DocumentRepository()

    def search(self, query: str, top_k: int = 3) -> list[DocumentChunk]:
        chunks = self.repository.load_chunks()

        scored_chunks = []

        for chunk in chunks:
            score = score_chunk(query, chunk)

            if score > 0:
                scored_chunks.append((score, chunk))

        scored_chunks.sort(key=lambda item: item[0], reverse=True)

        return [chunk for score, chunk in scored_chunks[:top_k]]