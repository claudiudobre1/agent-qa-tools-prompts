from typing import Literal, TypedDict


DataSource = Literal["rag", "csv", "sql", "fallback"]


class DataReaderState(TypedDict):
    query: str
    source: DataSource | None
    retry_count: int
    result: str | None
    error: str | None