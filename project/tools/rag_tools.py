from project.documents.rag_service import RAGService
from project.tools.params_models import SearchDocumentsParams
from project.tools.registry import register_tool


@register_tool(
    name="search_documents",
    description="Searches loaded documents and returns relevant chunks.",
    params_model=SearchDocumentsParams,
)
def search_documents(params: SearchDocumentsParams) -> str:
    service = RAGService()
    results = service.search(params.query, top_k=params.top_k)

    if not results:
        return "No relevant document chunks found."

    lines = [f"Found {len(results)} relevant chunk(s):"]

    for index, chunk in enumerate(results, start=1):
        lines.append(
            f"\n[{index}] {chunk.filename} | chunk {chunk.chunk_index}\n"
            f"{chunk.text}"
        )

    return "\n".join(lines)