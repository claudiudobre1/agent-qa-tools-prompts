from langgraph.graph import END, StateGraph

from project.graph.multi_agent_state import MultiAgentState
from project.graph.workers import (
    aggregate_results,
    csv_worker,
    fallback_worker,
    rag_worker,
    supervisor,
)


def route_after_supervisor(state: MultiAgentState) -> str:
    selected_agents = state["selected_agents"]

    if "rag_worker" in selected_agents:
        return "rag_worker"

    if "csv_worker" in selected_agents:
        return "csv_worker"

    return "fallback_worker"


def route_after_rag(state: MultiAgentState) -> str:
    selected_agents = state["selected_agents"]

    if "csv_worker" in selected_agents:
        return "csv_worker"

    return "aggregate_results"


def build_supervisor_graph():
    graph = StateGraph(MultiAgentState)

    graph.add_node("supervisor", supervisor)
    graph.add_node("rag_worker", rag_worker)
    graph.add_node("csv_worker", csv_worker)
    graph.add_node("fallback_worker", fallback_worker)
    graph.add_node("aggregate_results", aggregate_results)

    graph.set_entry_point("supervisor")

    graph.add_conditional_edges(
        "supervisor",
        route_after_supervisor,
        {
            "rag_worker": "rag_worker",
            "csv_worker": "csv_worker",
            "fallback_worker": "fallback_worker",
        },
    )

    graph.add_conditional_edges(
        "rag_worker",
        route_after_rag,
        {
            "csv_worker": "csv_worker",
            "aggregate_results": "aggregate_results",
        },
    )

    graph.add_edge("csv_worker", "aggregate_results")
    graph.add_edge("fallback_worker", "aggregate_results")
    graph.add_edge("aggregate_results", END)

    return graph.compile()


def run_supervisor(query: str) -> MultiAgentState:
    app = build_supervisor_graph()

    initial_state: MultiAgentState = {
        "query": query,
        "selected_agents": [],
        "agent_results": {},
        "final_answer": None,
        "error": None,
    }

    return app.invoke(initial_state)


if __name__ == "__main__":
    result = run_supervisor(
        "What does the contract say about termination notice and show csv rows?"
    )
    print(result["final_answer"])