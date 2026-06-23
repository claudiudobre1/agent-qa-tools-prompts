from mcp.server.fastmcp import FastMCP

from project.guardrails.validator import validate_query
from project.graph.data_reader_graph import run_data_reader
from project.graph.supervisor_graph import run_supervisor


mcp = FastMCP("Agent QA Tools MCP Server")


def format_data_reader_result(query: str) -> str:
    result = run_data_reader(query)

    return (
        "Data Reader Graph Result\n"
        f"Source selected: {result['source']}\n"
        f"Retry count: {result['retry_count']}\n"
        f"Error: {result['error']}\n\n"
        f"Result:\n{result['result']}"
    )


def format_supervisor_result(query: str) -> str:
    result = run_supervisor(query)

    return result["final_answer"] or "No final answer produced."


def guarded_response(query: str, handler) -> dict:
    validation = validate_query(query)

    if not validation.allowed:
        return {
            "allowed": False,
            "result": f"Input blocked by guardrails: {validation.reason}",
        }

    try:
        result = handler(query)
    except Exception as error:
        return {
            "allowed": False,
            "result": f"Tool execution error: {error}",
        }

    return {
        "allowed": True,
        "result": result,
    }


@mcp.tool()
def data_analyst_agent(query: str) -> dict:
    """
    Run the Data Reader Agent on a user query.

    This tool routes the query through the LangGraph Data Reader workflow.
    It can answer from RAG documents, CSV data, or fallback routing.
    """
    return guarded_response(query, format_data_reader_result)


@mcp.tool()
def orchestrator_agent(query: str) -> dict:
    """
    Run the Orchestrator Agent on a user query.

    This tool routes the query through the supervisor-style multi-agent graph.
    It can call the RAG worker, CSV worker, or fallback worker.
    """
    return guarded_response(query, format_supervisor_result)


if __name__ == "__main__":
    mcp.run()