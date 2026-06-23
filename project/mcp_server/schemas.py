from pydantic import BaseModel, Field


class AgentQueryInput(BaseModel):
    query: str = Field(
        description="User query to send to the agent.",
        min_length=1,
        max_length=1000,
    )


class AgentToolOutput(BaseModel):
    allowed: bool = Field(description="Whether the request passed guardrails.")
    result: str = Field(description="Agent result or guardrail block reason.")