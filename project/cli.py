from project.agent import QAAgent
from project.documents.chunker import chunk_document
from project.documents.loaders import load_text_file
from project.documents.repository import DocumentRepository
from project.graph.data_reader_graph import run_data_reader


def ingest_document(path: str) -> str:
    document = load_text_file(path)
    chunks = chunk_document(document)

    repository = DocumentRepository()
    repository.save_document(document)
    repository.save_chunks(chunks)

    return (
        f"Ingested document: {document.filename}\n"
        f"Document ID: {document.id}\n"
        f"Chunks created: {len(chunks)}"
    )


def run_data_reader_command(question: str) -> str:
    result = run_data_reader(question)

    return (
        "Data Reader Graph Result\n"
        f"Source selected: {result['source']}\n"
        f"Retry count: {result['retry_count']}\n"
        f"Error: {result['error']}\n\n"
        f"Result:\n{result['result']}"
    )


def main() -> None:
    agent = QAAgent()

    print("Agent QA Tools Prompts")
    print("Type 'exit' or 'quit' to stop.")
    print("Use '/debug your question' to see the ReAct trace.")
    print("Use '/ingest path/to/file.txt' to load a document.")
    print("Use '/data your question' to run the LangGraph data reader.")
    print()

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in {"exit", "quit"}:
            print("Agent: Goodbye, meatbag.")
            break

        if not user_input:
            continue

        if user_input.startswith("/ingest "):
            path = user_input.replace("/ingest ", "", 1).strip()

            try:
                result = ingest_document(path)
            except Exception as error:
                result = f"Ingest error: {error}"

            print()
            print(result)
            print()
            continue

        if user_input.startswith("/data "):
            question = user_input.replace("/data ", "", 1).strip()

            try:
                result = run_data_reader_command(question)
            except Exception as error:
                result = f"Data reader error: {error}"

            print()
            print(result)
            print()
            continue

        debug = False
        question = user_input

        if user_input.startswith("/debug "):
            debug = True
            question = user_input.replace("/debug ", "", 1).strip()

        answer = agent.answer(question, debug=debug)

        print()
        print(answer)
        print()


if __name__ == "__main__":
    main()