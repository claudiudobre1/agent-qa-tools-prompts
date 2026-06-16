from langgraph.graph import END, StateGraph

from project.graph.data_reader_nodes import (
    check_result,
    decide_source,
    execute_query,
    generate_query,
    parse_query,
)
from project.graph.state import DataReaderState


MAX_RETRIES = 2


def should_retry_or_finish(state: DataReaderState) -> str:
    if state["error"] and state["retry_count"] < MAX_RETRIES:
        return "retry"

    return "finish"


def build_data_reader_graph():
    graph = StateGraph(DataReaderState)

    graph.add_node("parse_query", parse_query)
    graph.add_node("decide_source", decide_source)
    graph.add_node("generate_query", generate_query)
    graph.add_node("execute_query", execute_query)
    graph.add_node("check_result", check_result)

    graph.set_entry_point("parse_query")

    graph.add_edge("parse_query", "decide_source")
    graph.add_edge("decide_source", "generate_query")
    graph.add_edge("generate_query", "execute_query")
    graph.add_edge("execute_query", "check_result")

    graph.add_conditional_edges(
        "check_result",
        should_retry_or_finish,
        {
            "retry": "decide_source",
            "finish": END,
        },
    )

    return graph.compile()


def run_data_reader(query: str) -> DataReaderState:
    app = build_data_reader_graph()

    initial_state: DataReaderState = {
        "query": query,
        "source": None,
        "retry_count": 0,
        "result": None,
        "error": None,
    }

    return app.invoke(initial_state)


if __name__ == "__main__":
    result = run_data_reader("What does the contract say about termination notice?")
    print(result)