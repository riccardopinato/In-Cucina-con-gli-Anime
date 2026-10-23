from __future__ import annotations

import argparse
import io
import sys
from pathlib import Path

from recipe_authoring_lib import (
    RECIPE_ARTWORK_HARD_MAX_BYTES,
    RECIPE_ARTWORK_MAX_LONG_EDGE,
    RECIPE_ARTWORK_MIN_SHORT_EDGE,
    RECIPE_ARTWORK_TARGET_MAX_BYTES,
    load_asset_manifest,
)

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "authoring" / "assets" / "manifest.json"


def _load_pillow():
    try:
        from PIL import Image, ImageOps
    except ImportError as exc:
        raise RuntimeError(
            "Pillow is required for artwork materialization. "
            "Install the pinned CI dependency first."
        ) from exc
    return Image, ImageOps


def _encode_jpeg(image, quality: int) -> bytes:
    buffer = io.BytesIO()
    image.save(
        buffer,
        format="JPEG",
        quality=quality,
        optimize=True,
        progressive=True,
        subsampling=2,
    )
    return buffer.getvalue()


def optimize_asset(source: Path) -> tuple[bytes, int, int, int]:
    Image, ImageOps = _load_pillow()
    original = source.read_bytes()
    with Image.open(io.BytesIO(original)) as opened:
        image = ImageOps.exif_transpose(opened).convert("RGB")
        width, height = image.size
        if (
            len(original) <= RECIPE_ARTWORK_TARGET_MAX_BYTES
            and min(width, height) >= RECIPE_ARTWORK_MIN_SHORT_EDGE
            and max(width, height) <= RECIPE_ARTWORK_MAX_LONG_EDGE
        ):
            return original, width, height, 0

        long_edge = max(width, height)
        if long_edge > RECIPE_ARTWORK_MAX_LONG_EDGE:
            scale = RECIPE_ARTWORK_MAX_LONG_EDGE / long_edge
            image = image.resize(
                (
                    max(1, round(width * scale)),
                    max(1, round(height * scale)),
                ),
                Image.Resampling.LANCZOS,
            )

        width, height = image.size
        if min(width, height) < RECIPE_ARTWORK_MIN_SHORT_EDGE:
            raise RuntimeError(
                f"{source} short edge is {min(width, height)}px; "
                f"minimum is {RECIPE_ARTWORK_MIN_SHORT_EDGE}px"
            )

        best: bytes | None = None
        best_quality = 0
        for quality in range(90, 59, -2):
            candidate = _encode_jpeg(image, quality)
            if len(candidate) <= RECIPE_ARTWORK_TARGET_MAX_BYTES:
                best = candidate
                best_quality = quality
                break

        if best is None:
            best_quality = 58
            best = _encode_jpeg(image, best_quality)

        if len(best) > RECIPE_ARTWORK_HARD_MAX_BYTES:
            raise RuntimeError(
                f"{source} cannot reach the hard size limit "
                f"({len(best)} > {RECIPE_ARTWORK_HARD_MAX_BYTES}) "
                "without dropping below the approved quality floor"
            )
        return best, width, height, best_quality


def run(*, output_dir: Path | None, write: bool) -> int:
    assets = load_asset_manifest(MANIFEST)
    if not write and output_dir is None:
        raise RuntimeError("choose --write or --output-dir")

    for asset_id, asset in sorted(assets.items()):
        source = ROOT / str(asset["path"])
        payload, width, height, quality = optimize_asset(source)
        destination = (
            source
            if write
            else output_dir / source.name  # type: ignore[operator]
        )
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(payload)
        print(
            f"{asset_id}: {width}x{height}, q={quality}, "
            f"{len(payload)} bytes -> {destination}"
        )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Optimize canonical recipe artwork to the F3E budget."
    )
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    try:
        return run(
            output_dir=(
                args.output_dir.resolve()
                if args.output_dir is not None
                else None
            ),
            write=args.write,
        )
    except RuntimeError as exc:
        print(f"Artwork optimization FAILED: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
