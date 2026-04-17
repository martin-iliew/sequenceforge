from __future__ import annotations

import json
import re
from pathlib import Path

from models import InspectionReport, TargetCandidate
from workflow import derive_public_base_path

TEXT_SUFFIXES = {
    ".css",
    ".html",
    ".js",
    ".jsx",
    ".json",
    ".mjs",
    ".scss",
    ".svelte",
    ".ts",
    ".tsx",
    ".vue",
}
SKIP_DIRS = {
    ".git",
    ".next",
    ".nuxt",
    "build",
    "coverage",
    "dist",
    "node_modules",
    "output",
    "public",
    "static",
}
ROUTE_SUFFIX_BONUS = {
    "app/page.tsx": 8,
    "app/page.jsx": 8,
    "pages/index.tsx": 8,
    "pages/index.jsx": 8,
    "index.html": 8,
    "pages/index.vue": 8,
    "src/routes/+page.svelte": 8,
}


def inspect_project(project_root: Path, target_hint: str, frames_dest: Path) -> InspectionReport:
    root = Path(project_root)
    files = list(_iter_text_files(root))
    package_json = _load_package_json(root / "package.json")
    framework = _detect_framework(package_json, files)
    style_strategy = _detect_style_strategy(package_json, files, framework)
    gsap_files = _find_gsap_files(files)
    gsap_registration_file = _pick_gsap_registration_file(gsap_files)
    animation_pattern = _detect_animation_pattern(framework, gsap_registration_file)
    target_candidates = _rank_target_candidates(files, target_hint, framework, gsap_registration_file)

    notes = []
    if len(target_candidates) > 1 and target_candidates[0].score == target_candidates[1].score:
        notes.append("Multiple target candidates are tied; ask before editing.")
    if framework == "unknown":
        notes.append("Fallback to generic GSAP integration heuristics.")

    return InspectionReport(
        project_root=root,
        framework=framework,
        style_strategy=style_strategy,
        animation_pattern=animation_pattern,
        frames_url_base=derive_public_base_path(root, Path(frames_dest)),
        gsap_files=gsap_files,
        gsap_registration_file=gsap_registration_file,
        target_candidates=target_candidates,
        notes=notes,
    )


def _iter_text_files(root: Path):
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        yield path


def _load_package_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _detect_framework(package_json: dict, files: list[Path]) -> str:
    deps = {
        **package_json.get("dependencies", {}),
        **package_json.get("devDependencies", {}),
    }
    if "next" in deps:
        return "react-next"
    if "@sveltejs/kit" in deps:
        return "sveltekit"
    if "nuxt" in deps:
        return "vue-nuxt"
    if "react" in deps:
        return "react"
    if "vue" in deps:
        return "vue"
    if "svelte" in deps:
        return "svelte"
    if any(path.name == "index.html" for path in files):
        return "vanilla"
    return "unknown"


def _detect_style_strategy(package_json: dict, files: list[Path], framework: str) -> str:
    deps = {
        **package_json.get("dependencies", {}),
        **package_json.get("devDependencies", {}),
    }
    if "tailwindcss" in deps or any(path.name.startswith("tailwind.config") for path in files):
        return "tailwind"
    if any(path.name.endswith(".module.css") or path.name.endswith(".module.scss") for path in files):
        return "css-modules"
    if framework in {"vue", "vue-nuxt"}:
        if any("<style scoped" in path.read_text(encoding="utf-8") for path in files if path.suffix == ".vue"):
            return "scoped"
    if framework in {"svelte", "sveltekit"}:
        if any("<style" in path.read_text(encoding="utf-8") for path in files if path.suffix == ".svelte"):
            return "scoped"
    if any(path.suffix in {".css", ".scss"} for path in files):
        return "css"
    return "inline"


def _find_gsap_files(files: list[Path]) -> list[Path]:
    matches = []
    for path in files:
        if path.suffix == ".json":
            continue
        text = path.read_text(encoding="utf-8")
        if "gsap" in text or "ScrollTrigger" in text:
            matches.append(path)
    return matches


def _pick_gsap_registration_file(gsap_files: list[Path]) -> Path | None:
    if not gsap_files:
        return None
    for path in gsap_files:
        text = path.read_text(encoding="utf-8")
        if "registerPlugin" in text and "ScrollTrigger" in text:
            return path
    return gsap_files[0]


def _detect_animation_pattern(framework: str, gsap_registration_file: Path | None) -> str:
    if not gsap_registration_file:
        return "inline"
    path_text = gsap_registration_file.as_posix().lower()
    if framework == "vanilla":
        return "inline"
    if any(segment in path_text for segment in ("lib/", "hooks/", "compos", "animat")):
        return "module"
    return "inline"


def _rank_target_candidates(
    files: list[Path],
    target_hint: str,
    framework: str,
    gsap_registration_file: Path | None,
) -> list[TargetCandidate]:
    hint_tokens = [token for token in re.split(r"[^a-z0-9]+", target_hint.lower()) if token]
    candidates: list[TargetCandidate] = []

    for path in files:
        if path.suffix not in {".html", ".jsx", ".tsx", ".vue", ".svelte"}:
            continue

        text = path.read_text(encoding="utf-8")
        score = 0
        reasons: list[str] = []

        for token in hint_tokens:
            if token in path.as_posix().lower():
                score += 7
                reasons.append(f"path matches '{token}'")
            if token in text.lower():
                score += 3
                reasons.append(f"content matches '{token}'")

        for suffix, bonus in ROUTE_SUFFIX_BONUS.items():
            if path.as_posix().lower().endswith(suffix):
                score += bonus
                reasons.append("route entrypoint")
                break

        if framework == "vanilla" and path.name == "index.html":
            score += 4
            reasons.append("html host")
        if gsap_registration_file and path.parent == gsap_registration_file.parent:
            score += 2
            reasons.append("near gsap setup")

        if score > 0:
            candidates.append(TargetCandidate(path=path, score=score, reasons=reasons))

    if not candidates:
        fallback = next((path for path in files if path.name == "index.html"), None)
        if fallback is None:
            fallback = next((path for path in files if path.suffix in {".tsx", ".jsx", ".vue", ".svelte"}), Path())
        return [TargetCandidate(path=fallback, score=1, reasons=["fallback entrypoint"])]

    return sorted(candidates, key=lambda item: (-item.score, item.path.as_posix()))
