import json
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

        if any(word in lowered for word in ["calculate", "what is", "*", "+", "-", "/"]):
            return {
                "tool_name": "calculator",
                "arguments": {"expression": question},
            }

        if any(word in lowered for word in ["date", "time", "today", "now"]):
            return {
                "tool_name": "datetime",
                "arguments": {"timezone": None},
            }

        return {
            "tool_name": "text_stats",
            "arguments": {"text": question},
        }

    def answer(self, question: str) -> str:
        notes = []

        planner_prompt = self.prompts.render(
            "planner",
            question=question,
            tools=self.tools.catalog_as_text(),
        )

        notes.append("Planner prompt rendered.")
        notes.append(planner_prompt)

        action = self.choose_tool(question)
        tool_name = action["tool_name"]
        arguments = action["arguments"]

        observation = self.tools.call(tool_name, arguments)

        analyst_prompt = self.prompts.render(
            "analyst",
            question=question,
            tool_name=tool_name,
            observation=observation,
        )

        notes.append("Tool selected: " + tool_name)
        notes.append("Tool arguments: " + json.dumps(arguments))
        notes.append("Observation: " + observation)
        notes.append(analyst_prompt)

        final_prompt = self.prompts.render(
            "summary",
            question=question,
            notes="\n\n".join(notes),
        )

        return (
            "QUESTION:\n"
            f"{question}\n\n"
            "ACTION:\n"
            f"Used tool: {tool_name}\n\n"
            "OBSERVATION:\n"
            f"{observation}\n\n"
            "FINAL:\n"
            f"{final_prompt}"
        )


if __name__ == "__main__":
    agent = QAAgent()

    question = "What in God's name do you want now meatbag?"
    print(agent.answer(question))