"""Stage 2: Denoising (Gaussian blur) + contrast enhancement (CLAHE)."""

from __future__ import annotations

from typing import Tuple

import cv2
import numpy as np

from .config import Config


def preprocess(image_gray: np.ndarray, cfg: Config) -> Tuple[np.ndarray, np.ndarray]:
    """Return (gaussian_blurred, clahe_enhanced)."""
    k = cfg.get("preprocessing", "gaussian_kernel", 5)
    k = k if k % 2 == 1 else k + 1  # kernel size must be odd
    gaussian = cv2.GaussianBlur(image_gray, (k, k), 0)

    clip_limit = cfg.get("preprocessing", "clahe_clip_limit", 2.0)
    tile = cfg.get("preprocessing", "clahe_tile_grid", 8)
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(tile, tile))
    clahe_image = clahe.apply(gaussian)

    return gaussian, clahe_image
