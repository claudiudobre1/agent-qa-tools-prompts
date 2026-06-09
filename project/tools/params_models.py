from pydantic import BaseModel, Field


class CalculatorParams(BaseModel):
    expression: str = Field(
        description="A simple arithmetic expression, for example: '25 * 17'"
    )


class DateTimeParams(BaseModel):
    timezone: str | None = Field(
        default=None,
        description="Optional timezone name. If omitted, local system time is used."
    )


class TextStatsParams(BaseModel):
    text: str = Field(
        description="Text to analyze."
    )


class SearchDocumentsParams(BaseModel):
    query: str = Field(
        description="Search query used to find relevant document chunks."
    )
    top_k: int = Field(
        default=3,
        description="Maximum number of document chunks to return."
    )