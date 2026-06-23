from pydantic import BaseModel, Field


class GuardrailResult(BaseModel):
    allowed: bool = Field(description="Whether the input is allowed.")
    reason: str = Field(description="Reason for allowing or blocking the input.")