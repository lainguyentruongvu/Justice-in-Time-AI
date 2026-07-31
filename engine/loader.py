from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from .utils import read_text, render_variables


@dataclass(frozen=True)
class LoadedModule:
    name: str
    path: Path
    content: str


class ModuleLoader:
    def __init__(self, variables: dict[str, Any] | None = None):
        self.variables = variables or {}

    def load(self, file_path: Path) -> LoadedModule:
        content = render_variables(read_text(file_path), self.variables)
        return LoadedModule(name=file_path.stem, path=file_path, content=content)

    def load_many(self, paths: Iterable[Path]) -> list[LoadedModule]:
        return [self.load(path) for path in paths]
