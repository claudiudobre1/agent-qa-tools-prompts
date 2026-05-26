from pathlib import Path
from typing import Any

import yaml
from jinja2 import Template


class PromptRegistry:
    def __init__(self, prompts_dir: str | Path):
        self.prompts_dir = Path(prompts_dir)
        self.prompts: dict[str, dict[str, Any]] = {}
        self.load_prompts()

    def load_prompts(self) -> None:
        for path in self.prompts_dir.glob("*.yaml"):
            with open(path, "r", encoding="utf-8") as file:
                data = yaml.safe_load(file)

            if not data:
                continue

            name = data["name"]
            self.prompts[name] = data

    def render(self, name: str, **variables: Any) -> str:
        if name not in self.prompts:
            raise ValueError(f"Prompt '{name}' not found. Available: {self.list_prompts()}")

        template_text = self.prompts[name]["template"]
        template = Template(template_text)

        return template.render(**variables)

    def list_prompts(self) -> list[str]:
        return list(self.prompts.keys())