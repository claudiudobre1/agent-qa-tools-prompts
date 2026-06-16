from typing import TypedDict


class MultiAgentState(TypedDict):
    query: str
    selected_agents: list[str]
    agent_results: dict[str, str]
    final_answer: str | None
    error: str | None