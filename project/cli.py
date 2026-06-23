from project.agent import QAAgent
from project.cache.store import PromptCache
from project.documents.chunker import chunk_document
from project.documents.loaders import load_text_file
from project.documents.repository import DocumentRepository
from project.graph.data_reader_graph import run_data_reader
from project.graph.supervisor_graph import run_supervisor
from project.intent.classifier import IntentClassifier
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


def classify_intent(question: str, classifier: IntentClassifier) -> str:
    if not question.strip():
        return "text_stats"

    return classifier.predict(question)


def answer_with_cache(
    cache: PromptCache,
    cache_key: str,
    answer_function,
    cache_miss_prefix: bool = True,
) -> str:
    cached = cache.get(cache_key)

    if cached:
        return "[CACHE HIT]\n" + cached.response

    answer = answer_function()
    cache.set(cache_key, answer)

    if cache_miss_prefix:
        return "[CACHE MISS]\n" + answer

    return answer


def main() -> None:
    agent = QAAgent()
    memory = ConversationMemory()
    cache = PromptCache()
    intent_classifier = IntentClassifier()

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
    print("Use '/intent your question' to classify intent.")
    print("Use '/auto your question' to classify intent and route automatically.")
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

        if user_input.startswith("/intent "):
            question = user_input.replace("/intent ", "", 1).strip()
            intent = classify_intent(question, intent_classifier)

            print()
            print(f"Predicted intent: {intent}")
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

            result = answer_with_cache(
                cache=cache,
                cache_key=cache_key,
                answer_function=lambda: run_data_reader_command(question),
            )

            memory.add_message("user", question)
            memory.add_message("assistant", result)

            print()
            print(result)
            print()
            continue

        if user_input.startswith("/multi "):
            question = user_input.replace("/multi ", "", 1).strip()
            cache_key = f"multi:{question}"

            result = answer_with_cache(
                cache=cache,
                cache_key=cache_key,
                answer_function=lambda: run_multi_agent_command(question),
            )

            memory.add_message("user", question)
            memory.add_message("assistant", result)

            print()
            print(result)
            print()
            continue

        if user_input.startswith("/auto "):
            question = user_input.replace("/auto ", "", 1).strip()
            intent = classify_intent(question, intent_classifier)
            cache_key = f"auto:{intent}:{question}"

            def route_question() -> str:
                if intent == "multi":
                    routed_answer = run_multi_agent_command(question)
                elif intent in {"rag", "csv"}:
                    routed_answer = run_data_reader_command(question)
                else:
                    routed_answer = agent.answer(question, debug=False)

                return (
                    f"Predicted intent: {intent}\n"
                    f"Route used: {intent}\n\n"
                    f"{routed_answer}"
                )

            result = answer_with_cache(
                cache=cache,
                cache_key=cache_key,
                answer_function=route_question,
            )

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

        answer = answer_with_cache(
            cache=cache,
            cache_key=cache_key,
            answer_function=lambda: agent.answer(question, debug=debug),
        )

        memory.add_message("user", question)
        memory.add_message("assistant", answer)

        print()
        print(answer)
        print()


if __name__ == "__main__":
    main()