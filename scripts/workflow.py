from __future__ import annotations

from pathlib import Path

from models import SequenceJob

KNOWN_PUBLIC_ROOTS = ("public", "static")


def derive_public_base_path(project_root: Path, frames_dest: Path) -> str:
    project_root = Path(project_root)
    frames_dest = Path(frames_dest)

    try:
        relative = frames_dest.relative_to(project_root)
    except ValueError:
        return "/" + frames_dest.as_posix().strip("/")

    relative_parts = relative.parts
    if relative_parts and relative_parts[0] in KNOWN_PUBLIC_ROOTS:
        exposed = Path(*relative_parts[1:]).as_posix().strip("/")
        return f"/{exposed}" if exposed else "/"

    return "/" + relative.as_posix().strip("/")


def normalize_job(
    *,
    prompt: str,
    project_root: Path,
    target_hint: str,
    frames_dest: Path,
    generation_mode: str = "manual",
    fps: int = 30,
    duration_seconds: int = 4,
    canvas_id: str = "image-sequence",
    overwrite: bool = False,
) -> SequenceJob:
    normalized_mode = generation_mode.lower().strip() or "manual"
    if normalized_mode not in {"manual", "provider"}:
        raise ValueError(f"Unsupported generation mode: {generation_mode}")

    job = SequenceJob(
        prompt=prompt.strip(),
        project_root=Path(project_root),
        target_hint=target_hint.strip(),
        frames_dest=Path(frames_dest),
        generation_mode=normalized_mode,
        fps=int(fps),
        duration_seconds=int(duration_seconds),
        canvas_id=canvas_id.strip() or "image-sequence",
        overwrite=overwrite,
    )
    job.frames_url_base = derive_public_base_path(job.project_root, job.frames_dest)
    return job
