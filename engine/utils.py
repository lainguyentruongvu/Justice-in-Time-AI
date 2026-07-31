from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any


def read_text(file_path: Path) -> str:
    if not file_path.exists():
        raise FileNotFoundError(f"Module not found: {file_path}")
    return file_path.read_text(encoding="utf-8").strip()


def render_variables(text: str, variables: dict[str, Any] | None = None) -> str:
    variables = variables or {}

    def replace(match: re.Match[str]) -> str:
        key = match.group(1).strip()
        return str(variables.get(key, match.group(0)))

    return re.sub(r"\{\{\s*([\w.-]+)\s*\}\}", replace, text)


def estimate_tokens(text: str) -> int:
    # Safe dependency-free approximation for English/Vietnamese prompts.
    return max(1, len(text) // 4)


def load_variables(path: Path | None) -> dict[str, Any]:
    if path is None:
        return {}
    if not path.exists():
        raise FileNotFoundError(f"Variables file not found: {path}")
    if path.suffix.lower() != ".json":
        raise ValueError("Variables file must be JSON.")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Variables JSON must contain an object.")
    return data


def save_output(output_dir: Path, task: str, content: str) -> Path:
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = output_dir / f"{task}_{stamp}.md"
    path.write_text(content, encoding="utf-8")
    return path
