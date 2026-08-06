"""Stage 6/7/8 visualizations."""

from __future__ import annotations

from typing import List

import cv2
import numpy as np

from .components import Component


def draw_components(mask: np.ndarray, components: List[Component]) -> np.ndarray:
    output = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    for c in components:
        x, y, w, h = c.bbox
        cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.circle(output, c.centroid, 5, (0, 0, 255), -1)
    return output


def draw_numbered(mask: np.ndarray, ordered_components: List[Component]) -> np.ndarray:
    output = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    for idx, c in enumerate(ordered_components, start=1):
        cx, cy = c.centroid
        cv2.circle(output, (cx, cy), 5, (0, 0, 255), -1)
        cv2.putText(output, str(idx), (cx - 10, cy - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    return output


def overlay_on_original(image_gray: np.ndarray, ordered_components: List[Component]) -> np.ndarray:
    """Draw the numbered bones on top of the *original* image (not just the
    binary mask), which is far more useful for visual verification against
    real anatomy than an isolated mask."""
    output = cv2.cvtColor(image_gray, cv2.COLOR_GRAY2BGR)
    for idx, c in enumerate(ordered_components, start=1):
        x, y, w, h = c.bbox
        cx, cy = c.centroid
        cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 1)
        cv2.circle(output, (cx, cy), 4, (0, 0, 255), -1)
        cv2.putText(output, str(idx), (cx - 10, cy - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
    return output


def edge_qc_overlay(image_gray: np.ndarray, edges: np.ndarray, final_mask: np.ndarray) -> np.ndarray:
    """Diagnostic image: Canny edges in red, final mask boundary in green,
    both drawn over the original grayscale image, so you can visually judge
    whether the segmentation boundary tracks genuine intensity edges."""
    output = cv2.cvtColor(image_gray, cv2.COLOR_GRAY2BGR)
    output[edges > 0] = (0, 0, 255)  # red = canny edges
    contours, _ = cv2.findContours(final_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(output, contours, -1, (0, 255, 0), 1)  # green = mask boundary
    return output


def make_comparison_grid(images_titled: List[tuple], cols: int = 4, cell_size: int = 200) -> np.ndarray:
    """Build a labeled grid image from a list of (title, image) pairs, for a
    single at-a-glance QC image of every pipeline stage."""
    cells = []
    for title, img in images_titled:
        if img.ndim == 2:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        resized = cv2.resize(img, (cell_size, cell_size))
        cv2.putText(resized, title, (5, 18), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
        cells.append(resized)

    rows = []
    for i in range(0, len(cells), cols):
        row_cells = cells[i:i + cols]
        while len(row_cells) < cols:
            row_cells.append(np.zeros((cell_size, cell_size, 3), dtype=np.uint8))
        rows.append(np.hstack(row_cells))
    return np.vstack(rows)
