import re
from pathlib import Path
from typing import Any

from project.prompts.registry import PromptRegistry
from project.tools import ToolWrapper


class QAAgent:
    def __init__(self):
        prompts_dir = Path(__file__).parent / "prompts"
        self.prompts = PromptRegistry(prompts_dir)
        self.tools = ToolWrapper

    def choose_tool(self, question: str) -> dict[str, Any]:
        lowered = question.lower()

        time_keywords = ["time", "date", "today"]
        if any(keyword in lowered for keyword in time_keywords):
            return {
                "tool_name": "datetime",
                "arguments": {"timezone": None},
            }

        math_pattern = r"[\d\s+\-*/().%]+"
        possible_expressions = re.findall(math_pattern, question)

        for expression in possible_expressions:
            expression = expression.strip()

            has_digit = any(char.isdigit() for char in expression)
            has_operator = any(char in expression for char in ["+", "-", "*", "/", "%"])

            if has_digit and has_operator:
                return {
                    "tool_name": "calculator",
                    "arguments": {"expression": expression},
                }

        return {
            "tool_name": "text_stats",
            "arguments": {"text": question},
        }

    def answer(self, question: str) -> str:
        action = self.choose_tool(question)
        tool_name = action["tool_name"]
        arguments = action["arguments"]

        observation = self.tools.call(tool_name, arguments)

        return (
            f"Tool used: {tool_name}\n"
            f"Result: {observation}"
        )


if __name__ == "__main__":
    agent = QAAgent()

    question = "What in God's name do you want now meatbag?"
    print(agent.answer(question))