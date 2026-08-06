"""Image loading/saving helpers with real error handling (no bare exit())."""

from __future__ import annotations

from pathlib import Path
from typing import List

import cv2
import numpy as np

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff"}


class ImageLoadError(RuntimeError):
    """Raised when an image cannot be read from disk."""


def load_grayscale(image_path: Path) -> np.ndarray:
    image_path = Path(image_path)
    if not image_path.exists():
        raise ImageLoadError(f"Image not found: {image_path}")
    image = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ImageLoadError(
            f"OpenCV failed to decode image (unsupported/corrupt file?): {image_path}"
        )
    return image


def load_color(image_path: Path) -> np.ndarray:
    image_path = Path(image_path)
    if not image_path.exists():
        raise ImageLoadError(f"Image not found: {image_path}")
    image = cv2.imread(str(image_path), cv2.IMREAD_COLOR)
    if image is None:
        raise ImageLoadError(
            f"OpenCV failed to decode image (unsupported/corrupt file?): {image_path}"
        )
    return image


def save_image(image: np.ndarray, out_path: Path) -> None:
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    ok = cv2.imwrite(str(out_path), image)
    if not ok:
        raise RuntimeError(f"Failed to write image to: {out_path}")


def list_images(folder: Path) -> List[Path]:
    folder = Path(folder)
    if not folder.exists():
        raise FileNotFoundError(f"Dataset folder does not exist: {folder}")
    files = sorted(
        p for p in folder.iterdir()
        if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS
    )
    if not files:
        raise FileNotFoundError(f"No supported images found in: {folder}")
    return files
