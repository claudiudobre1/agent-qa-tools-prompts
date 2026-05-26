from typing import Callable, Any


TOOL_REGISTRY: dict[str, dict[str, Any]] = {}


def register_tool(
    name: str,
    description: str,
    params_model: type
):
    """
    Decorator used to register a tool with metadata.
    """

    def decorator(func: Callable):
        TOOL_REGISTRY[name] = {
            "name": name,
            "description": description,
            "params_model": params_model,
            "function": func,
        }
        return func

    return decorator


def get_tool(name: str) -> dict[str, Any]:
    if name not in TOOL_REGISTRY:
        raise ValueError(f"Tool '{name}' not found.")

    return TOOL_REGISTRY[name]


def list_tools() -> list[dict[str, Any]]:
    return [
        {
            "name": tool["name"],
            "description": tool["description"],
            "parameters": tool["params_model"].model_json_schema(),
        }
        for tool in TOOL_REGISTRY.values()
    ]