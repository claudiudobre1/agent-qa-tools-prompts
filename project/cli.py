from project.agent import QAAgent


def main() -> None:
    agent = QAAgent()

    print("Agent QA Tools Prompts")
    print("Type 'exit' or 'quit' to stop.")
    print("Use '/debug your question' to see the ReAct trace.")
    print()

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in {"exit", "quit"}:
            print("Agent: Goodbye, meatbag.")
            break

        if not user_input:
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