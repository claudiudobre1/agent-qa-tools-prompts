import json
from pathlib import Path

from project.memory.models import MemoryMessage


class ConversationMemory:
    def __init__(self, path: str | Path = "data/memory.json"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

        if not self.path.exists():
            self.path.write_text("[]", encoding="utf-8")

    def add_message(self, role: str, content: str) -> None:
        messages = self.load_messages()
        messages.append(MemoryMessage(role=role, content=content))

        self.path.write_text(
            json.dumps([message.model_dump() for message in messages], indent=2),
            encoding="utf-8",
        )

    def load_messages(self) -> list[MemoryMessage]:
        data = json.loads(self.path.read_text(encoding="utf-8"))
        return [MemoryMessage(**item) for item in data]

    def last_messages(self, limit: int = 6) -> list[MemoryMessage]:
        return self.load_messages()[-limit:]

    def clear(self) -> None:
        self.path.write_text("[]", encoding="utf-8")

    def as_text(self, limit: int = 6) -> str:
        messages = self.last_messages(limit=limit)

        if not messages:
            return "No conversation memory yet."

        return "\n".join(
            f"{message.role}: {message.content}" for message in messages
        )