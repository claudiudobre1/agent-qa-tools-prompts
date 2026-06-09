from project.tools import ToolWrapper
from project.documents.chunker import chunk_document, chunk_text
from project.documents.loaders import load_text_file
from project.documents.repository import DocumentRepository
from project.documents.rag_service import RAGService


def test_load_text_file():
    document = load_text_file("data/sample_docs/contract.txt")

    assert document.filename == "contract.txt"
    assert "terminated with 30 days written notice" in document.text


def test_chunk_text_creates_chunks():
    text = (
        "First paragraph used for testing.\n\n"
        "Second paragraph used for testing.\n\n"
        "Third paragraph used for testing."
    )

    chunks = chunk_text(
        text,
        chunk_size=50,
        overlap=5,
    )

    assert len(chunks) > 1


def test_chunk_text_keeps_paragraphs_intact():
    text = (
        "This contract can be terminated with 30 days written notice.\n\n"
        "The client must pay all invoices within 15 days."
    )

    chunks = chunk_text(
        text,
        chunk_size=80,
        overlap=10,
    )

    assert chunks[0] == "This contract can be terminated with 30 days written notice."
    assert chunks[1] == "The client must pay all invoices within 15 days."


def test_chunk_document_creates_document_chunks():
    document = load_text_file("data/sample_docs/contract.txt")
    chunks = chunk_document(document, chunk_size=80, overlap=10)

    assert len(chunks) > 0
    assert chunks[0].document_id == document.id
    assert chunks[0].filename == "contract.txt"


def test_repository_saves_and_loads_documents(tmp_path):
    document = load_text_file("data/sample_docs/contract.txt")
    chunks = chunk_document(document, chunk_size=80, overlap=10)

    repository = DocumentRepository(data_dir=tmp_path)
    repository.save_document(document)
    repository.save_chunks(chunks)

    loaded_documents = repository.load_documents()
    loaded_chunks = repository.load_chunks()

    assert len(loaded_documents) == 1
    assert len(loaded_chunks) == len(chunks)


def test_rag_service_finds_relevant_chunks(tmp_path):
    document = load_text_file("data/sample_docs/contract.txt")
    chunks = chunk_document(document, chunk_size=80, overlap=10)

    repository = DocumentRepository(data_dir=tmp_path)
    repository.save_document(document)
    repository.save_chunks(chunks)

    service = RAGService(repository=repository)
    results = service.search("termination notice", top_k=2)

    assert len(results) > 0
    assert "terminated" in results[0].text


def test_search_documents_tool_returns_relevant_chunks(tmp_path):
    document = load_text_file("data/sample_docs/contract.txt")
    chunks = chunk_document(document, chunk_size=80, overlap=10)

    repository = DocumentRepository(data_dir=tmp_path)
    repository.save_document(document)
    repository.save_chunks(chunks)

    # Patch the default repository data by using the real data folder
    real_repository = DocumentRepository()
    real_repository.save_document(document)
    real_repository.save_chunks(chunks)

    result = ToolWrapper.call(
        "search_documents",
        {
            "query": "termination notice",
            "top_k": 2,
        },
    )

    assert "Found" in result
    assert "contract.txt" in result
    assert "terminated with 30 days written notice" in result