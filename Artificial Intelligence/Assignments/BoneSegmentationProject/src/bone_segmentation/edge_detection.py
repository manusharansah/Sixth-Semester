"""
Stage 3: Canny edge detection.

NOTE on scope: in the original project this step produced an edge map that
was computed but never actually consumed by any later stage - i.e. dead
code. Here it is kept as an explicit, clearly-labeled QC/diagnostic step:
the edge map is not fed into segmentation (Otsu thresholding is a more
robust segmentation cue for these images), but it IS used to build a
diagnostic overlay so you can visually sanity-check how well the final
mask boundary follows genuine intensity edges in the image.
"""

from __future__ import annotations

import cv2
import numpy as np

from .config import Config


def detect_edges(image_gray: np.ndarray, cfg: Config) -> np.ndarray:
    low = cfg.get("edge_detection", "canny_low", 50)
    high = cfg.get("edge_detection", "canny_high", 150)
    return cv2.Canny(image_gray, low, high)
