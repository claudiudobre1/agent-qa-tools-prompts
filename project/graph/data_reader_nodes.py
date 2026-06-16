import pandas as pd

from project.documents.rag_service import RAGService
from project.graph.state import DataReaderState


def parse_query(state: DataReaderState) -> DataReaderState:
    query = state["query"].strip()

    return {
        **state,
        "query": query,
        "error": None if query else "Query is empty.",
    }


def decide_source(state: DataReaderState) -> DataReaderState:
    query = state["query"].lower()

    if state["error"]:
        return {
            **state,
            "source": "fallback",
        }

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
        source = "rag"
    elif any(keyword in query for keyword in csv_keywords):
        source = "csv"
    else:
        source = "fallback"

    return {
        **state,
        "source": source,
    }


def generate_query(state: DataReaderState) -> DataReaderState:
    return {
        **state,
        "query": state["query"],
    }


def execute_query(state: DataReaderState) -> DataReaderState:
    source = state["source"]

    if source == "rag":
        service = RAGService()
        results = service.search(state["query"], top_k=3)

        if not results:
            return {
                **state,
                "result": None,
                "error": "No RAG results found.",
            }

        text_results = []

        for index, chunk in enumerate(results, start=1):
            text_results.append(
                f"[{index}] {chunk.filename} | chunk {chunk.chunk_index}\n"
                f"{chunk.text}"
            )

        return {
            **state,
            "result": "\n\n".join(text_results),
            "error": None,
        }

    if source == "csv":
        try:
            dataframe = pd.read_csv("data/sample_docs/sample.csv")

            result = (
                f"CSV loaded successfully.\n"
                f"Rows: {len(dataframe)}\n"
                f"Columns: {list(dataframe.columns)}"
            )

            return {
                **state,
                "result": result,
                "error": None,
            }

        except Exception as error:
            return {
                **state,
                "result": None,
                "error": f"CSV error: {error}",
            }

    return {
        **state,
        "result": "Fallback: no suitable data source was selected.",
        "error": None,
    }


def check_result(state: DataReaderState) -> DataReaderState:
    if state["result"]:
        return {
            **state,
            "error": None,
        }

    retry_count = state["retry_count"] + 1

    return {
        **state,
        "retry_count": retry_count,
        "error": state["error"] or "No result produced.",
    }