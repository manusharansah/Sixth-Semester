"""
Stage 6: Connected-component analysis.

Includes an optional watershed step to split bones that are touching /
overlapping and would otherwise be merged into a single connected
component by simple thresholding + morphology (a known limitation of the
original pipeline).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

import cv2
import numpy as np
from scipy import ndimage as ndi
from skimage.feature import peak_local_max
from skimage.segmentation import watershed

from .config import Config


@dataclass
class Component:
    label: int
    area: int
    bbox: tuple  # (x, y, w, h)
    centroid: tuple  # (cx, cy)


def find_components(clean_mask: np.ndarray, cfg: Config) -> List[Component]:
    if cfg.get("components", "use_watershed", False):
        labels = _watershed_split(clean_mask, cfg)
    else:
        num_labels, labels_arr = cv2.connectedComponents(clean_mask)
        labels = labels_arr

    min_area = cfg.get("morphology", "min_area", 500)
    components: List[Component] = []
    max_label = labels.max()
    for lbl in range(1, max_label + 1):
        region = (labels == lbl)
        area = int(region.sum())
        if area <= min_area:
            continue
        ys, xs = np.where(region)
        x, y, w, h = xs.min(), ys.min(), xs.max() - xs.min() + 1, ys.max() - ys.min() + 1
        cx, cy = int(xs.mean()), int(ys.mean())
        components.append(Component(label=lbl, area=area, bbox=(int(x), int(y), int(w), int(h)),
                                     centroid=(cx, cy)))
    return components


def _watershed_split(mask: np.ndarray, cfg: Config) -> np.ndarray:
    """Separate touching blobs using a distance-transform + watershed."""
    distance = ndi.distance_transform_edt(mask)
    min_distance = cfg.get("components", "watershed_min_distance", 15)
    coords = peak_local_max(distance, min_distance=min_distance, labels=mask.astype(bool))
    peak_mask = np.zeros_like(distance, dtype=bool)
    peak_mask[tuple(coords.T)] = True
    markers, _ = ndi.label(peak_mask)
    labels = watershed(-distance, markers, mask=mask.astype(bool))
    return labels
