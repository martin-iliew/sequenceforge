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


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect a GSAP project for image-sequence integration")
    parser.add_argument("--project-root", required=True, help="Project root to inspect")
    parser.add_argument("--target-hint", required=True, help="Page/component/section hint")
    parser.add_argument("--frames-dest", required=True, help="Destination folder for extracted frames")
    args = parser.parse_args()

    report = inspect_project(
        project_root=Path(args.project_root),
        target_hint=args.target_hint,
        frames_dest=Path(args.frames_dest),
    )

    print(json.dumps(asdict(report), indent=2, default=str))


if __name__ == "__main__":
    main()
