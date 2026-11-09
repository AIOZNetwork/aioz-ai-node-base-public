"""Task pipeline stages: preprocess -> predict -> postprocess.

These stages ship as a runnable placeholder that writes a solid-color PNG, so
`python preflight.py` works out of the box. Replace each stage's body with your
logic. Keep the stage boundaries or reshape them for your task.
"""

import struct
import zlib
from pathlib import Path
from typing import Any, Dict, Tuple


def preprocess(prompt: str, negative_prompt: str, seed: int) -> Dict[str, Any]:
    """Turn the raw input into model-ready parameters.

    Placeholder: pass the generation parameters through unchanged.
    """
    return {"prompt": prompt, "negative_prompt": negative_prompt, "seed": seed}


def predict(model: Any, params: Dict[str, Any]) -> bytes:
    """Run the model and return the generated image as PNG bytes.

    Placeholder: build a solid-color PNG from the seed (no model). Replace with
    your model, e.g. encode `model(**params).images[0]` to PNG bytes.
    """
    seed = int(params["seed"])
    rgb = (seed & 0xFF, (seed >> 8) & 0xFF, (seed >> 16) & 0xFF)
    return _solid_png(64, 64, rgb)


def postprocess(image_bytes: bytes) -> Path:
    """Write the image bytes to a file and return its path."""
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / "image.png"
    output_path.write_bytes(image_bytes)
    return output_path


def _solid_png(width: int, height: int, rgb: Tuple[int, int, int]) -> bytes:
    """Encode a solid-color RGB image as PNG bytes using only the stdlib."""

    def chunk(tag: bytes, data: bytes) -> bytes:
        crc = zlib.crc32(tag + data) & 0xFFFFFFFF
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", crc)

    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)  # 8-bit RGB
    raw = (b"\x00" + bytes(rgb) * width) * height  # filter byte 0 per row
    return (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", ihdr)
        + chunk(b"IDAT", zlib.compress(raw))
        + chunk(b"IEND", b"")
    )
