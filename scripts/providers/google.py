from __future__ import annotations

import os
import sys
import time
from pathlib import Path

from .base import ProviderConfigError, ensure_parent_dir


class GoogleProvider:
    def check_env(self) -> None:
        try:
            from google import genai  # noqa: F401
        except ImportError as exc:
            raise ProviderConfigError("google-genai not installed. Run: pip install google-genai") from exc

        missing = [
            name
            for name in ("GOOGLE_CLOUD_PROJECT", "GOOGLE_APPLICATION_CREDENTIALS")
            if not os.environ.get(name)
        ]
        if missing:
            raise ProviderConfigError(f"Missing env vars: {', '.join(missing)}")

    def generate_image(self, prompt: str, spec: dict, output_path: str, label: str) -> bytes:
        from google import genai
        from google.genai import types

        client = genai.Client()
        model = spec["meta"]["imagen_model"]
        image_size = spec["meta"].get("image_size", "2K")
        aspect_ratio = spec["meta"]["aspect_ratio"]
        max_retries = spec["meta"].get("max_retries", 3)

        for attempt in range(max_retries):
            try:
                response = client.models.generate_images(
                    model=model,
                    prompt=prompt,
                    config=types.GenerateImagesConfig(
                        number_of_images=1,
                        aspect_ratio=aspect_ratio,
                        image_size=image_size,
                    ),
                )
                image_bytes = response.generated_images[0].image.image_bytes
                ensure_parent_dir(output_path)
                Path(output_path).write_bytes(image_bytes)
                size_kb = len(image_bytes) // 1024
                print(f"  Saved {label}: {output_path} ({size_kb} KB)")
                return image_bytes
            except Exception as exc:  # pragma: no cover - provider behavior is external
                if "safety" in str(exc).lower() or "blocked" in str(exc).lower():
                    print(f"  Safety block on {label}: {exc}", file=sys.stderr)
                    print("  Adjust the prompt in frame-spec.yaml and rerun.", file=sys.stderr)
                    sys.exit(2)
                if attempt < max_retries - 1:
                    wait = 2**attempt
                    print(f"  Retry {attempt + 1} in {wait}s: {exc}")
                    time.sleep(wait)
                else:
                    raise
        raise RuntimeError("Image generation failed")

    def generate_video(self, spec: dict, first_bytes: bytes, last_bytes: bytes, output_path: str) -> None:
        from google import genai
        from google.genai import types

        client = genai.Client()
        model = spec["meta"]["veo_model"]
        duration = int(spec["meta"].get("duration_seconds", 4))
        aspect_ratio = spec["meta"].get("aspect_ratio", "16:9")
        transition_prompt = spec["transition"]["assembled_prompt"]
        max_retries = spec["meta"].get("max_retries", 3)

        first_image = types.Image(image_bytes=first_bytes, mime_type="image/png")
        last_image = types.Image(image_bytes=last_bytes, mime_type="image/png")
        operation = None

        for attempt in range(max_retries):
            try:
                operation = client.models.generate_videos(
                    model=model,
                    prompt=transition_prompt,
                    image=first_image,
                    config=types.GenerateVideosConfig(
                        last_frame=last_image,
                        duration_seconds=duration,
                        aspect_ratio=aspect_ratio,
                    ),
                )
                break
            except Exception as exc:  # pragma: no cover - provider behavior is external
                if attempt < max_retries - 1:
                    wait = 2**attempt
                    print(f"  Veo submit retry {attempt + 1} in {wait}s: {exc}")
                    time.sleep(wait)
                else:
                    raise

        if operation is None:
            raise RuntimeError("Video generation did not return an operation.")

        op_file = Path(output_path).parent / "pending-operation.txt"
        if getattr(operation, "name", None):
            op_file.write_text(operation.name, encoding="utf-8")
            print(f"  Operation ID: {operation.name}")

        print("  Waiting for Veo (3-5 min typical)...", end="", flush=True)
        deadline = time.time() + 600
        while not operation.done:  # pragma: no cover - provider behavior is external
            if time.time() > deadline:
                print()
                raise TimeoutError(
                    f"Veo timed out. Operation ID saved to {op_file} for manual retrieval."
                )
            time.sleep(10)
            operation = client.operations.get(operation)
            print(".", end="", flush=True)
        print(" done")

        video_bytes = operation.result.generated_videos[0].video.video_bytes
        ensure_parent_dir(output_path)
        Path(output_path).write_bytes(video_bytes)

        if op_file.exists():
            op_file.unlink()

        size_mb = len(video_bytes) / 1_000_000
        print(f"  Saved video: {output_path} ({size_mb:.1f} MB)")
