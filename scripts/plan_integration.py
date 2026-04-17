#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from inspection import inspect_project
from integration import build_integration_blueprint
from workflow import normalize_job


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a framework-aware GSAP image-sequence blueprint")
    parser.add_argument("--prompt", required=True, help="Visual sequence intent")
    parser.add_argument("--project-root", required=True, help="Project root to inspect")
    parser.add_argument("--target-hint", required=True, help="Page/component/section hint")
    parser.add_argument("--frames-dest", required=True, help="Destination folder for extracted frames")
    parser.add_argument("--generation-mode", default="manual", choices=("manual", "provider"))
    parser.add_argument("--fps", type=int, default=30)
    parser.add_argument("--duration", type=int, default=4)
    parser.add_argument("--canvas-id", default="image-sequence")
    args = parser.parse_args()

    job = normalize_job(
        prompt=args.prompt,
        project_root=Path(args.project_root),
        target_hint=args.target_hint,
        frames_dest=Path(args.frames_dest),
        generation_mode=args.generation_mode,
        fps=args.fps,
        duration_seconds=args.duration,
        canvas_id=args.canvas_id,
    )
    report = inspect_project(job.project_root, job.target_hint, job.frames_dest)
    blueprint = build_integration_blueprint(job, report)
    print(json.dumps(asdict(blueprint), indent=2, default=str))


if __name__ == "__main__":
    main()
