from __future__ import annotations

from pathlib import Path

import yaml


PROJECT_SETUP_FIELDS = (
    "framework",
    "visual_tone",
    "motion_intensity",
    "motion_appetite",
    "motion_no_go",
    "must_have_motion",
    "color_direction",
    "constraints",
)


def project_setup_path(project_root: Path) -> Path:
    return Path(project_root) / "docs" / "design" / "project-setup.yaml"


def load_project_setup(project_root: Path) -> dict:
    path = project_setup_path(project_root)
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return {str(key): value for key, value in data.items()}


def save_project_setup(project_root: Path, answers: dict) -> Path:
    path = project_setup_path(project_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    normalized = {field: answers.get(field, "") for field in PROJECT_SETUP_FIELDS}
    path.write_text(yaml.safe_dump(normalized, sort_keys=False), encoding="utf-8")
    return path


def missing_project_setup_fields(project_root: Path) -> list[str]:
    config = load_project_setup(project_root)
    return [field for field in PROJECT_SETUP_FIELDS if not config.get(field)]


def should_ask_project_setup_questions(project_root: Path) -> bool:
    config = load_project_setup(project_root)
    return (not config) or ("framework" not in config) or bool(missing_project_setup_fields(project_root))
