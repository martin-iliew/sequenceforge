#!/usr/bin/env python3
"""
sequenceforge — generate.py

Generates keyframe images (Imagen 4) and a bridging video (Veo 3.1) from frame-spec.yaml.
All model and generation settings are read from the spec.

Usage:
    python scripts/generate.py
    python scripts/generate.py --spec output/frame-spec.yaml --output-dir output
    python scripts/generate.py --mock

Flags:
    --spec        Path to frame-spec.yaml  (default: output/frame-spec.yaml)
    --output-dir  Where to write outputs   (default: output)
    --mock        Skip all API calls. Generates gradient PNGs + ffmpeg crossfade. Free.
"""

import argparse
import struct
import subprocess
import sys
import zlib
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import yaml

from providers import GoogleProvider, ProviderConfigError


def load_yaml(path: str) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


# ---------------------------------------------------------------------------
# Mock mode — no API, no cost, tests the full pipeline
# ---------------------------------------------------------------------------

def _png_chunk(name: bytes, data: bytes) -> bytes:
    chunk = name + data
    return struct.pack(">I", len(data)) + chunk + struct.pack(">I", zlib.crc32(chunk) & 0xFFFFFFFF)


def _make_gradient_png(width: int, height: int, top_rgb: tuple, bottom_rgb: tuple) -> bytes:
    raw_rows = []
    for y in range(height):
        t = y / max(height - 1, 1)
        r = int(top_rgb[0] + t * (bottom_rgb[0] - top_rgb[0]))
        g = int(top_rgb[1] + t * (bottom_rgb[1] - top_rgb[1]))
        b = int(top_rgb[2] + t * (bottom_rgb[2] - top_rgb[2]))
        row = b"\x00" + bytes([r, g, b] * width)
        raw_rows.append(row)
    compressed = zlib.compress(b"".join(raw_rows), 9)
    return (
        b"\x89PNG\r\n\x1a\n"
        + _png_chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
        + _png_chunk(b"IDAT", compressed)
        + _png_chunk(b"IEND", b"")
    )


def mock_generate(spec: dict, output_dir: Path) -> tuple[bytes, bytes]:
    duration = int(spec["meta"].get("duration_seconds", 4))

    print("  [MOCK] Placeholder first frame (warm gradient)...")
    first_bytes = _make_gradient_png(320, 180, (255, 200, 100), (180, 100, 40))
    first_path = output_dir / "frame-first.png"
    first_path.write_bytes(first_bytes)
    print(f"  Saved: {first_path}")

    print("  [MOCK] Placeholder last frame (cool gradient)...")
    last_bytes = _make_gradient_png(320, 180, (40, 80, 160), (20, 180, 120))
    last_path = output_dir / "frame-last.png"
    last_path.write_bytes(last_bytes)
    print(f"  Saved: {last_path}")

    print("  [MOCK] Test video (ffmpeg crossfade)...")
    video_path = output_dir / "video.mp4"
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-t", str(duration), "-i", str(first_path),
        "-loop", "1", "-t", str(duration), "-i", str(last_path),
        "-filter_complex",
        f"[0][1]xfade=transition=fade:duration={duration}:offset=0,format=yuv420p",
        "-t", str(duration), str(video_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg failed:\n{result.stderr}")

    size_kb = video_path.stat().st_size // 1024
    print(f"  Saved: {video_path} ({size_kb} KB)")
    print("  [MOCK] Cost: $0.00")
    return first_bytes, last_bytes


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Generate keyframes + video via Google Imagen 4 and Veo 3.1")
    parser.add_argument("--spec", default="output/frame-spec.yaml", help="Path to frame-spec.yaml")
    parser.add_argument("--output-dir", default="output", help="Output directory")
    parser.add_argument("--mock", action="store_true", help="Skip APIs, generate placeholders. Free.")
    args = parser.parse_args()

    spec = load_yaml(args.spec)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    first_path = output_dir / "frame-first.png"
    last_path = output_dir / "frame-last.png"
    video_path = output_dir / "video.mp4"

    if args.mock:
        print("\n[MOCK MODE] No API calls. Cost: $0.00\n")
        mock_generate(spec, output_dir)

    else:
        provider = GoogleProvider()
        try:
            provider.check_env()
        except ProviderConfigError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            sys.exit(1)

        print("[1/3] Generating first frame (Imagen 4)...")
        first_bytes = provider.generate_image(
            spec["first_frame"]["assembled_prompt"],
            spec,
            str(first_path),
            "frame-first.png",
        )

        print("\n[2/3] Generating last frame (Imagen 4)...")
        last_bytes = provider.generate_image(
            spec["last_frame"]["assembled_prompt"],
            spec,
            str(last_path),
            "frame-last.png",
        )

        print("\n[3/3] Generating video (Veo 3.1)...")
        provider.generate_video(spec, first_bytes, last_bytes, str(video_path))

    print("\nAll done.")
    print(f"  {first_path}")
    print(f"  {last_path}")
    print(f"  {video_path}")
    print("\nNext: extract frames")
    print(f"  python scripts/extract_frames.py --input {video_path} --dest public/images/frames")


if __name__ == "__main__":
    main()
