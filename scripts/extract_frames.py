#!/usr/bin/env python3
"""
sequenceforge — extract_frames.py

Extracts lossless PNG frames from a video using ffmpeg.
Output format: frame_000001.png, frame_000002.png, ...

Usage:
    python scripts/extract_frames.py --input output/video.mp4 --dest public/images/frames
    python scripts/extract_frames.py --input output/video.mp4 --dest public/images/frames --fps 24

Why lossless PNG:
    Scroll sequences display one frame at a time. JPEG compression introduces
    artifacts that appear as visible flicker between consecutive frames.
    PNG with -compression_level 0 preserves every pixel exactly as rendered.

Requirements:
    ffmpeg must be installed and on PATH.
"""

import argparse
import subprocess
import sys
from pathlib import Path


def check_ffmpeg() -> None:
    result = subprocess.run(
        ["ffmpeg", "-version"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print("ERROR: ffmpeg not found or not on PATH.", file=sys.stderr)
        print("\nInstall ffmpeg:", file=sys.stderr)
        print("  macOS:   brew install ffmpeg", file=sys.stderr)
        print("  Ubuntu:  sudo apt install ffmpeg", file=sys.stderr)
        print("  Windows: https://ffmpeg.org/download.html (add to PATH)", file=sys.stderr)
        sys.exit(1)


def extract_frames(input_path: str, dest_dir: str, fps: float | None = None) -> int:
    """
    Extract frames from video as lossless PNG files.

    Args:
        input_path: Path to the input video file.
        dest_dir:   Directory to write frame_XXXXXX.png files.
        fps:        Frames per second to extract. If None, uses source fps.

    Returns:
        Number of frames extracted.
    """
    input_path = Path(input_path)
    dest_dir = Path(dest_dir)

    # Validate input
    if not input_path.exists():
        raise FileNotFoundError(f"Video not found: {input_path}")
    if input_path.stat().st_size == 0:
        raise ValueError(f"Video file is empty: {input_path}")

    dest_dir.mkdir(parents=True, exist_ok=True)
    output_pattern = str(dest_dir / "frame_%06d.png")

    # Build ffmpeg command
    # -y           overwrite without asking
    # -i           input file
    # -vf fps=N    resample to N fps (omit to keep source rate)
    # -compression_level 0  lossless PNG (no compression artifacts)
    # frame_%06d.png  zero-padded 6-digit counter
    cmd = ["ffmpeg", "-y", "-i", str(input_path)]
    if fps is not None:
        cmd += ["-vf", f"fps={fps}"]
    cmd += ["-compression_level", "0", output_pattern]

    print(f"Input:  {input_path}")
    print(f"Output: {dest_dir}/frame_XXXXXX.png")
    if fps:
        print(f"FPS:    {fps}")
    else:
        print("FPS:    source (native frame rate)")
    print()

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print("ffmpeg error:", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        raise RuntimeError(f"ffmpeg exited with code {result.returncode}")

    # Count and report
    frames = sorted(dest_dir.glob("frame_*.png"))
    if not frames:
        raise RuntimeError(
            "No frames were extracted. "
            "The video may be corrupt or in an unsupported format.\n"
            f"ffmpeg output:\n{result.stderr}"
        )

    print(f"Extracted {len(frames)} frames")
    print(f"  First: {frames[0].name}")
    print(f"  Last:  {frames[-1].name}")
    print(f"  Path:  {dest_dir}/")

    return len(frames)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract lossless PNG frames from a video file"
    )
    parser.add_argument(
        "--input", required=True,
        help="Path to input video file (e.g. output/video.mp4)"
    )
    parser.add_argument(
        "--dest", required=True,
        help="Output directory for PNG frames (e.g. public/images/frames)"
    )
    parser.add_argument(
        "--fps", type=float, default=None,
        help="Frame rate for extraction (default: source fps)"
    )
    args = parser.parse_args()

    check_ffmpeg()
    extract_frames(args.input, args.dest, args.fps)


if __name__ == "__main__":
    main()
