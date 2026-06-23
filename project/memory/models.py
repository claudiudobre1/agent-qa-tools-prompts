from datetime import datetime
from pydantic import BaseModel, Field


class MemoryMessage(BaseModel):
    role: str = Field(description="Message role, for example user or assistant.")
    content: str = Field(description="Message content.")
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())