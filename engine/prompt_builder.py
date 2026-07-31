from __future__ import annotations

from typing import Any

from .loader import ModuleLoader
from .registry import get_task
from .utils import estimate_tokens


class PromptBuilder:
    def __init__(self, task: str, variables: dict[str, Any] | None = None):
        self.task = task
        self.variables = variables or {}

    def build(self) -> str:
        task_spec = get_task(self.task)
        modules = ModuleLoader(self.variables).load_many(task_spec.modules)

        sections = [
            "# JUSTICE IN TIME AI — COMPILED SYSTEM PROMPT",
            f"Task: {self.task}",
            f"Purpose: {task_spec.description}",
            "Follow later modules when instructions conflict, except global safety and factuality rules.",
        ]

        for index, module in enumerate(modules, start=1):
            sections.append(
                f"\n\n{'=' * 72}\n"
                f"MODULE {index}: {module.name}\n"
                f"SOURCE: {module.path.name}\n"
                f"{'=' * 72}\n\n"
                f"{module.content}"
            )

        prompt = "\n".join(sections).strip()
        return prompt

    def token_estimate(self) -> int:
        return estimate_tokens(self.build())
