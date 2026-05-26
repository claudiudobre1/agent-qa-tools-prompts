import json
from typing import Any

from project.tools.registry import get_tool, list_tools


class ToolWrapper:
    """
    Executes registered tools safely using their Pydantic parameter models.
    """

    @staticmethod
    def catalog() -> list[dict[str, Any]]:
        return list_tools()

    @staticmethod
    def call(tool_name: str, arguments: dict[str, Any]) -> str:
        try:
            tool = get_tool(tool_name)
            params_model = tool["params_model"]
            function = tool["function"]

            params = params_model(**arguments)
            return function(params)

        except Exception as error:
            return f"Tool error: {error}"

    @staticmethod
    def catalog_as_text() -> str:
        tools = ToolWrapper.catalog()

        lines = []
        for tool in tools:
            schema = json.dumps(tool["parameters"], indent=2)
            lines.append(
                f"Tool: {tool['name']}\n"
                f"Description: {tool['description']}\n"
                f"Parameters:\n{schema}"
            )

        return "\n\n".join(lines)