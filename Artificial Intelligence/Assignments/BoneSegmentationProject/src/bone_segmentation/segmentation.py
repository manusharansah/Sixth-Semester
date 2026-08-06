"""Stage 4: Binary segmentation (Otsu global threshold or adaptive threshold)."""

from __future__ import annotations

from typing import Tuple

import cv2
import numpy as np

from .config import Config


def segment(image_gray: np.ndarray, cfg: Config) -> Tuple[np.ndarray, float]:
    """Return (binary_mask, threshold_value_used).

    threshold_value_used is -1 for adaptive thresholding, since there is no
    single global value in that mode.
    """
    method = cfg.get("segmentation", "method", "otsu")

    if method == "adaptive":
        block_size = cfg.get("segmentation", "adaptive_block_size", 35)
        if block_size % 2 == 0:
            block_size += 1
        c = cfg.get("segmentation", "adaptive_c", 5)
        binary = cv2.adaptiveThreshold(
            image_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, block_size, c,
        )
        return binary, -1.0

    # default: otsu
    threshold_value, binary = cv2.threshold(
        image_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )
    return binary, float(threshold_value)
