"""Stage 5: Morphological cleanup - opening, closing, hole filling, small-object removal."""

from __future__ import annotations

import cv2
import numpy as np

from .config import Config


def clean_mask(binary: np.ndarray, cfg: Config) -> np.ndarray:
    ksize = cfg.get("morphology", "kernel_size", 5)
    kernel = np.ones((ksize, ksize), np.uint8)

    opening = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)

    if cfg.get("morphology", "fill_holes", True):
        closing = _fill_holes(closing)

    min_area = cfg.get("morphology", "min_area", 500)
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(closing)
    clean = np.zeros_like(closing)
    for i in range(1, num_labels):
        area = stats[i, cv2.CC_STAT_AREA]
        if area > min_area:
            clean[labels == i] = 255

    return clean


def _fill_holes(binary: np.ndarray) -> np.ndarray:
    """Fill enclosed dark holes inside white bone regions via flood fill."""
    h, w = binary.shape
    flood = binary.copy()
    mask = np.zeros((h + 2, w + 2), np.uint8)
    cv2.floodFill(flood, mask, (0, 0), 255)
    flood_inv = cv2.bitwise_not(flood)
    return binary | flood_inv
