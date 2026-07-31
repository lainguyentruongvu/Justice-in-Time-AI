"""Application configuration and project paths."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv


# ==========================================
# PROJECT PATHS
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = PROJECT_ROOT / ".env"

CORE = PROJECT_ROOT / "00_CORE"
COMMENT = PROJECT_ROOT / "01_COMMENT"
CONTENT = PROJECT_ROOT / "02_CONTENT"
SEO = PROJECT_ROOT / "03_SEO"
ANALYTICS = PROJECT_ROOT / "04_ANALYTICS"
DATA = PROJECT_ROOT / "05_DATA"
WORKFLOWS = PROJECT_ROOT / "06_WORKFLOWS"

OUTPUTS = PROJECT_ROOT / "outputs"
OUTPUTS.mkdir(parents=True, exist_ok=True)


# ==========================================
# ENVIRONMENT VARIABLES
# ==========================================

load_dotenv(
    dotenv_path=ENV_FILE,
    override=True,
)


def clean_env(name: str, default: str = "") -> str:
    """Read and clean a string environment variable."""
    return (
        os.getenv(name, default)
        .strip()
        .strip('"')
        .strip("'")
    )


def get_int_env(name: str, default: int) -> int:
    """Read an integer environment variable safely."""
    raw_value = clean_env(name, str(default))

    try:
        return int(raw_value)
    except ValueError:
        return default


def get_float_env(name: str, default: float) -> float:
    """Read a float environment variable safely."""
    raw_value = clean_env(name, str(default))

    try:
        return float(raw_value)
    except ValueError:
        return default


# ==========================================
# GEMINI CONFIGURATION
# ==========================================

GEMINI_API_KEY = clean_env("GEMINI_API_KEY")

MODEL = clean_env(
    "GEMINI_MODEL",
    "gemini-3.6-flash",
)

MAX_OUTPUT_TOKENS = get_int_env(
    "MAX_OUTPUT_TOKENS",
    4000,
)

TEMPERATURE = get_float_env(
    "TEMPERATURE",
    0.7,
)