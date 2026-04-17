from __future__ import annotations

from pathlib import Path
from typing import Protocol


class ProviderConfigError(RuntimeError):
    """Raised when a provider is not configured correctly."""


class VideoProvider(Protocol):
    def check_env(self) -> None: ...

    def generate_image(self, prompt: str, spec: dict, output_path: str, label: str) -> bytes: ...

    def generate_video(
        self,
        spec: dict,
        first_bytes: bytes,
        last_bytes: bytes,
        output_path: str,
    ) -> None: ...


def ensure_parent_dir(path: str | Path) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
