from project.agent import QAAgent


def main() -> None:
    agent = QAAgent()

    print("Agent QA Tools Prompts")
    print("Type 'exit' or 'quit' to stop.")
    print()

    while True:
        question = input("You: ").strip()

        if question.lower() in {"exit", "quit"}:
            print("Agent: Goodbye, meatbag.")
            break

        if not question:
            continue

        answer = agent.answer(question)
        print()
        print(answer)
        print()


if __name__ == "__main__":
    main()