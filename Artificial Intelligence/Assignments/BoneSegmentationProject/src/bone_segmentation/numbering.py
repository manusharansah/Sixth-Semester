"""
Stage 7: Assign reproducible numbers to detected bone components.

The original project numbered components in whatever arbitrary order
cv2.connectedComponentsWithStats happened to return labels in, which is an
implementation detail and not visually meaningful. Here components are
sorted into a stable "reading order" (top-to-bottom, then left-to-right)
by default, or by descending area, so the same image always produces the
same numbering and the numbering is intuitive to a human reader.
"""

from __future__ import annotations

from typing import List

from .components import Component
from .config import Config


def order_components(components: List[Component], cfg: Config) -> List[Component]:
    sort_by = cfg.get("numbering", "sort_by", "reading_order")

    if sort_by == "area_desc":
        return sorted(components, key=lambda c: c.area, reverse=True)

    # reading_order: bucket by row (using a coarse y-band) then sort by x
    row_height = 40  # px band; groups components that are roughly on the same row
    return sorted(
        components,
        key=lambda c: (c.centroid[1] // row_height, c.centroid[0]),
    )
