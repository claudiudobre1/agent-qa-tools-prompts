import hashlib
import json
from datetime import datetime
from pathlib import Path

from project.cache.models import CacheEntry


class PromptCache:
    def __init__(self, path: str | Path = "data/cache.json"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

        if not self.path.exists():
            self.path.write_text("[]", encoding="utf-8")

    def make_key(self, query: str) -> str:
        normalized = query.strip().lower()
        return hashlib.sha256(normalized.encode("utf-8")).hexdigest()

    def load_entries(self) -> list[CacheEntry]:
        data = json.loads(self.path.read_text(encoding="utf-8"))
        return [CacheEntry(**item) for item in data]

    def get(self, query: str) -> CacheEntry | None:
        key = self.make_key(query)
        entries = self.load_entries()

        for entry in entries:
            if entry.key == key:
                entry.hit_count += 1
                entry.updated_at = datetime.now().isoformat()
                self.save_entry(entry)
                return entry

        return None

    def set(self, query: str, response: str) -> CacheEntry:
        key = self.make_key(query)
        entries = self.load_entries()

        entries = [entry for entry in entries if entry.key != key]

        entry = CacheEntry(
            key=key,
            query=query,
            response=response,
        )

        entries.append(entry)
        self.path.write_text(
            json.dumps([item.model_dump() for item in entries], indent=2),
            encoding="utf-8",
        )

        return entry

    def save_entry(self, updated_entry: CacheEntry) -> None:
        entries = self.load_entries()
        new_entries = []

        for entry in entries:
            if entry.key == updated_entry.key:
                new_entries.append(updated_entry)
            else:
                new_entries.append(entry)

        self.path.write_text(
            json.dumps([item.model_dump() for item in new_entries], indent=2),
            encoding="utf-8",
        )

    def clear(self) -> None:
        self.path.write_text("[]", encoding="utf-8")

    def stats(self) -> str:
        entries = self.load_entries()
        total_hits = sum(entry.hit_count for entry in entries)

        return (
            f"Cache entries: {len(entries)}\n"
            f"Total cache hits: {total_hits}"
        )