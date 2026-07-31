from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .config import ANALYTICS, COMMENT, CONTENT, CORE, DATA, SEO, WORKFLOWS

CORE_MODULES = [
    CORE / "jit_CORE.md",
    CORE / "jit_BRAND.md",
    CORE / "jit_STYLE.md",
    CORE / "jit_RULES.md",
]


@dataclass(frozen=True)
class TaskSpec:
    description: str
    modules: tuple[Path, ...]


def spec(description: str, *modules: Path) -> TaskSpec:
    return TaskSpec(description=description, modules=tuple(CORE_MODULES + list(modules)))


REGISTRY: dict[str, TaskSpec] = {
    "jit_comment": spec("Generate engaging audience comments", COMMENT / "jit_comment.md", DATA / "audience_profile.md", DATA / "viral_comments.md"),
    "jit_reply": spec("Reply naturally as the channel creator", COMMENT / "jit_reply.md", DATA / "audience_profile.md", DATA / "viral_comments.md"),
    "jit_hook": spec("Create a high-retention video hook", CONTENT / "jit_hook.md", DATA / "audience_profile.md"),
    "jit_script": spec("Create a complete True Crime documentary script", CONTENT / "jit_script.md", DATA / "audience_profile.md", DATA / "prompt_history.md"),
    "jit_community": spec("Create a YouTube community post", CONTENT / "jit_community.md", DATA / "audience_profile.md"),
    "jit_titlevideo": spec("Generate high-CTR YouTube titles", SEO / "jit_titlevideo.md", DATA / "title_examples.md", DATA / "audience_profile.md"),
    "jit_desc": spec("Create an optimized YouTube description", SEO / "jit_desc.md", DATA / "audience_profile.md"),
    "jit_ctr": spec("Analyze click-through rate and packaging", ANALYTICS / "jit_ctr.md", DATA / "title_examples.md"),
    "jit_retention": spec("Analyze audience retention", ANALYTICS / "jit_retention.md", DATA / "audience_profile.md"),
    "jit_analytics": spec("Analyze overall channel/video performance", ANALYTICS / "jit_analytics.md", DATA / "audience_profile.md", DATA / "prompt_history.md"),
    "workflow_comment": spec("Run the comment workflow", WORKFLOWS / "workflow_comment.md", COMMENT / "jit_comment.md", COMMENT / "jit_reply.md", DATA / "audience_profile.md", DATA / "viral_comments.md"),
    "workflow_video": spec("Run the video production workflow", WORKFLOWS / "workflow_video.md", CONTENT / "jit_hook.md", CONTENT / "jit_script.md", SEO / "jit_titlevideo.md", SEO / "jit_desc.md", DATA / "audience_profile.md", DATA / "title_examples.md"),
    "workflow_analytics": spec("Run the analytics workflow", WORKFLOWS / "workflow_analytics.md", ANALYTICS / "jit_ctr.md", ANALYTICS / "jit_retention.md", ANALYTICS / "jit_analytics.md", DATA / "audience_profile.md"),
    "workflow_upload": spec("Prepare a video upload package", WORKFLOWS / "workflow_upload.md", SEO / "jit_titlevideo.md", SEO / "jit_desc.md", DATA / "title_examples.md", DATA / "audience_profile.md"),
    "workflow_complete": spec("Run the complete Justice in Time workflow", WORKFLOWS / "workflow_complete.md", CONTENT / "jit_hook.md", CONTENT / "jit_script.md", SEO / "jit_titlevideo.md", SEO / "jit_desc.md", COMMENT / "jit_comment.md", COMMENT / "jit_reply.md", ANALYTICS / "jit_ctr.md", ANALYTICS / "jit_retention.md", ANALYTICS / "jit_analytics.md", DATA / "audience_profile.md", DATA / "title_examples.md", DATA / "viral_comments.md", DATA / "prompt_history.md"),
}


def get_task(name: str) -> TaskSpec:
    try:
        return REGISTRY[name]
    except KeyError as exc:
        available = ", ".join(sorted(REGISTRY))
        raise KeyError(f"Unknown task '{name}'. Available: {available}") from exc
