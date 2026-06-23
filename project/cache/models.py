from datetime import datetime
from pydantic import BaseModel, Field


class CacheEntry(BaseModel):
    key: str = Field(description="Unique cache key.")
    query: str = Field(description="Original user query.")
    response: str = Field(description="Cached response.")
    hit_count: int = Field(default=0)
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now().isoformat())