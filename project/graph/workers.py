import pandas as pd

from project.documents.rag_service import RAGService
from project.graph.multi_agent_state import MultiAgentState


def supervisor(state: MultiAgentState) -> MultiAgentState:
    query = state["query"].lower()
    selected_agents = []

    rag_keywords = [
        "document",
        "contract",
        "clause",
        "termination",
        "notice",
        "file",
    ]

    csv_keywords = [
        "csv",
        "table",
        "rows",
        "columns",
        "average",
        "sum",
        "data",
    ]

    if any(keyword in query for keyword in rag_keywords):
        selected_agents.append("rag_worker")

    if any(keyword in query for keyword in csv_keywords):
        selected_agents.append("csv_worker")

    if not selected_agents:
        selected_agents.append("fallback_worker")

    return {
        **state,
        "selected_agents": selected_agents,
        "error": None,
    }


def rag_worker(state: MultiAgentState) -> MultiAgentState:
    service = RAGService()
    results = service.search(state["query"], top_k=3)

    agent_results = dict(state["agent_results"])

    if not results:
        agent_results["rag_worker"] = "No RAG results found."
    else:
        chunks = []

        for index, chunk in enumerate(results, start=1):
            chunks.append(
                f"[{index}] {chunk.filename} | chunk {chunk.chunk_index}\n"
                f"{chunk.text}"
            )

        agent_results["rag_worker"] = "\n\n".join(chunks)

    return {
        **state,
        "agent_results": agent_results,
    }


def csv_worker(state: MultiAgentState) -> MultiAgentState:
    agent_results = dict(state["agent_results"])

    try:
        dataframe = pd.read_csv("data/sample_docs/sample.csv")

        agent_results["csv_worker"] = (
            f"CSV loaded successfully.\n"
            f"Rows: {len(dataframe)}\n"
            f"Columns: {list(dataframe.columns)}"
        )

    except Exception as error:
        agent_results["csv_worker"] = f"CSV error: {error}"

    return {
        **state,
        "agent_results": agent_results,
    }


def fallback_worker(state: MultiAgentState) -> MultiAgentState:
    agent_results = dict(state["agent_results"])
    agent_results["fallback_worker"] = (
        "Fallback worker: no specialized agent was selected."
    )

    return {
        **state,
        "agent_results": agent_results,
    }


def aggregate_results(state: MultiAgentState) -> MultiAgentState:
    lines = ["Multi-Agent Orchestration Result"]

    for agent_name in state["selected_agents"]:
        result = state["agent_results"].get(agent_name, "No result produced.")

        lines.append(
            f"\nAgent: {agent_name}\n"
            f"{result}"
        )

    return {
        **state,
        "final_answer": "\n".join(lines),
        "error": None,
    }