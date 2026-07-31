from __future__ import annotations

import argparse
import sys
from pathlib import Path

from engine.config import MODEL, OUTPUTS
from engine.prompt_builder import PromptBuilder
from engine.registry import REGISTRY
from engine.runner import RunnerError, run
from engine.utils import load_variables, save_output


def print_tasks() -> None:
    print("\nAvailable tasks:\n")
    for index, (name, task) in enumerate(REGISTRY.items(), start=1):
        print(f"  {index:>2}. {name:<22} {task.description}")


def choose_task() -> str:
    tasks = list(REGISTRY)
    print_tasks()
    value = input("\nSelect task number or name: ").strip()
    if value.isdigit():
        index = int(value) - 1
        if 0 <= index < len(tasks):
            return tasks[index]
    if value in REGISTRY:
        return value
    raise ValueError(f"Invalid task: {value}")


def read_multiline_input() -> str:
    print("\nPaste your input. Finish with a line containing only END:\n")
    lines: list[str] = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line.strip() == "END":
            break
        lines.append(line)
    return "\n".join(lines).strip()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Justice in Time modular AI engine")
    parser.add_argument("task", nargs="?", choices=list(REGISTRY), help="Task to run")
    parser.add_argument("--input", "-i", dest="input_file", type=Path, help="Read user input from a UTF-8 text file")
    parser.add_argument("--text", "-t", help="Provide user input directly")
    parser.add_argument("--variables", "-v", type=Path, help="JSON file containing {{variables}}")
    parser.add_argument("--model", default=MODEL, help="Override GEMINI_MODEL")
    parser.add_argument("--show-prompt", action="store_true", help="Print the compiled system prompt and exit")
    parser.add_argument("--no-save", action="store_true", help="Do not save output to outputs/")
    parser.add_argument("--list", action="store_true", help="List available tasks and exit")
    return parser


def main() -> int:
    args = build_parser().parse_args()

    print("=" * 64)
    print("JUSTICE IN TIME AI — GEMINI ENGINE v2.1")
    print("=" * 64)

    if args.list:
        print_tasks()
        return 0

    try:
        task = args.task or choose_task()
        variables = load_variables(args.variables)
        builder = PromptBuilder(task, variables)
        system_prompt = builder.build()

        print(f"\nTask: {task}")
        print(f"Model: {args.model}")
        print(f"Estimated system prompt tokens: {builder.token_estimate():,}")

        if args.show_prompt:
            print("\n" + system_prompt)
            return 0

        if args.text is not None:
            user_input = args.text
        elif args.input_file is not None:
            user_input = args.input_file.read_text(encoding="utf-8")
        else:
            user_input = read_multiline_input()

        print("\nGenerating...\n")
        result = run(system_prompt, user_input, model=args.model)
        print(result)

        if not args.no_save:
            path = save_output(OUTPUTS, task, result)
            print(f"\nSaved: {path.relative_to(path.parent.parent)}")
        return 0

    except (ValueError, KeyError, FileNotFoundError, RunnerError) as exc:
        print(f"\nERROR: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nCancelled.")
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
