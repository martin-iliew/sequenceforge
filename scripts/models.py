from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(slots=True)
class SequenceJob:
    prompt: str
    project_root: Path
    target_hint: str
    frames_dest: Path
    generation_mode: str = "manual"
    fps: int = 30
    duration_seconds: int = 4
    canvas_id: str = "image-sequence"
    overwrite: bool = False
    frames_url_base: str = ""


@dataclass(slots=True)
class TargetCandidate:
    path: Path
    score: int
    reasons: list[str] = field(default_factory=list)


@dataclass(slots=True)
class InspectionReport:
    project_root: Path
    framework: str
    style_strategy: str
    animation_pattern: str
    frames_url_base: str
    gsap_files: list[Path]
    gsap_registration_file: Path | None
    target_candidates: list[TargetCandidate]
    notes: list[str] = field(default_factory=list)


@dataclass(slots=True)
class IntegrationBlueprint:
    framework: str
    animation_host_strategy: str
    target_file: Path
    animation_file: Path
    style_file: Path | None
    frame_count: int
    canvas_markup: str
    style_snippet: str
    animation_code: str
    helper_code: str
    notes: list[str] = field(default_factory=list)


@dataclass(slots=True)
class IntegrationApplyResult:
    blueprint: IntegrationBlueprint
    changed_files: list[str]
