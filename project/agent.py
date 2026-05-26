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

    def answer(self, question: str, debug: bool = False) -> str:
        max_iterations = 3
        trace = []

        planner_prompt = self.prompts.render(
            "planner",
            question=question,
            tools=self.tools.catalog_as_text(),
        )

        trace.append("Think: Read the user question and inspect available tools.")
        trace.append("Planner prompt rendered successfully.")
        trace.append(planner_prompt)

        for iteration in range(1, max_iterations + 1):
            action = self.choose_tool(question)
            tool_name = action["tool_name"]
            arguments = action["arguments"]

            trace.append(
                f"Act {iteration}: Call tool '{tool_name}' with arguments {arguments}."
            )

            observation = self.tools.call(tool_name, arguments)

            trace.append(f"Observe {iteration}: {observation}")

            analyst_prompt = self.prompts.render(
                "analyst",
                question=question,
                tool_name=tool_name,
                observation=observation,
            )

            trace.append("Analyst prompt rendered successfully.")
            trace.append(analyst_prompt)

            tool_failed = observation.startswith("Error") or observation.startswith(
                "Tool error"
            )

            if not tool_failed:
                final_answer = (
                    f"Tool used: {tool_name}\n"
                    f"Result: {observation}"
                )

                if debug:
                    return (
                        "REACT TRACE:\n"
                        + "\n\n".join(trace)
                        + "\n\nFINAL ANSWER:\n"
                        + final_answer
                    )

                return final_answer

            trace.append(
                f"Think {iteration}: Tool failed, retrying if another iteration is available."
            )

        failure_message = "I could not produce an answer within the iteration limit."

        if debug:
            return (
                "REACT TRACE:\n"
                + "\n\n".join(trace)
                + "\n\nFINAL ANSWER:\n"
                + failure_message
            )

        return failure_message


if __name__ == "__main__":
    agent = QAAgent()

    question = "What in God's name do you want now meatbag?"
    print(agent.answer(question))