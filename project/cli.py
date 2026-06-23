from project.agent import QAAgent
from project.cache.store import PromptCache
from project.documents.chunker import chunk_document
from project.documents.loaders import load_text_file
from project.documents.repository import DocumentRepository
from project.graph.data_reader_graph import run_data_reader
from project.graph.supervisor_graph import run_supervisor
from project.memory.store import ConversationMemory


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


def run_multi_agent_command(question: str) -> str:
    result = run_supervisor(question)

    return result["final_answer"] or "No final answer produced."


def main() -> None:
    agent = QAAgent()
    memory = ConversationMemory()
    cache = PromptCache()

    print("Agent QA Tools Prompts")
    print("Type 'exit' or 'quit' to stop.")
    print("Use '/debug your question' to see the ReAct trace.")
    print("Use '/ingest path/to/file.txt' to load a document.")
    print("Use '/data your question' to run the LangGraph data reader.")
    print("Use '/multi your question' to run the multi-agent supervisor.")
    print("Use '/memory' to show recent conversation memory.")
    print("Use '/memory clear' to clear conversation memory.")
    print("Use '/cache' to show prompt cache stats.")
    print("Use '/cache clear' to clear prompt cache.")
    print()

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in {"exit", "quit"}:
            print("Agent: Goodbye, meatbag.")
            break

        if user_input == "":
            continue

        if user_input == "/memory":
            print()
            print(memory.as_text())
            print()
            continue

        if user_input == "/memory clear":
            memory.clear()
            print()
            print("Conversation memory cleared.")
            print()
            continue

        if user_input == "/cache":
            print()
            print(cache.stats())
            print()
            continue

        if user_input == "/cache clear":
            cache.clear()
            print()
            print("Prompt cache cleared.")
            print()
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
            cache_key = f"data:{question}"
            cached = cache.get(cache_key)

            if cached:
                result = "[CACHE HIT]\n" + cached.response
            else:
                try:
                    result = run_data_reader_command(question)
                except Exception as error:
                    result = f"Data reader error: {error}"

                cache.set(cache_key, result)
                result = "[CACHE MISS]\n" + result

            memory.add_message("user", question)
            memory.add_message("assistant", result)

            print()
            print(result)
            print()
            continue

        if user_input.startswith("/multi "):
            question = user_input.replace("/multi ", "", 1).strip()
            cache_key = f"multi:{question}"
            cached = cache.get(cache_key)

            if cached:
                result = "[CACHE HIT]\n" + cached.response
            else:
                try:
                    result = run_multi_agent_command(question)
                except Exception as error:
                    result = f"Multi-agent error: {error}"

                cache.set(cache_key, result)
                result = "[CACHE MISS]\n" + result

            memory.add_message("user", question)
            memory.add_message("assistant", result)

            print()
            print(result)
            print()
            continue

        debug = False
        question = user_input

        if user_input.startswith("/debug "):
            debug = True
            question = user_input.replace("/debug ", "", 1).strip()

        cache_key = f"agent:{question}:debug={debug}"
        cached = cache.get(cache_key)

        if cached:
            answer = "[CACHE HIT]\n" + cached.response
        else:
            answer = agent.answer(question, debug=debug)
            cache.set(cache_key, answer)
            answer = "[CACHE MISS]\n" + answer

        memory.add_message("user", question)
        memory.add_message("assistant", answer)

        print()
        print(answer)
        print()


if __name__ == "__main__":
    main()