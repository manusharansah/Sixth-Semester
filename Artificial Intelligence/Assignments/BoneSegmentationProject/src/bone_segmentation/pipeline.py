"""End-to-end pipeline orchestration for a single image."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional

from . import components as components_mod
from . import edge_detection, io_utils, metrics, morphology_ops, numbering
from . import preprocessing, segmentation, visualization
from .config import Config


def run_pipeline(
    image_path: Path,
    output_dir: Path,
    cfg: Config,
    logger: logging.Logger,
    ground_truth_path: Optional[Path] = None,
    show: bool = False,
) -> Dict[str, Any]:
    """Run the full pipeline on a single image and write all artifacts to
    output_dir/<image_stem>/. Returns a summary dict (also written as
    summary.json alongside the images)."""

    image_path = Path(image_path)
    stem = image_path.stem
    run_dir = Path(output_dir) / stem
    run_dir.mkdir(parents=True, exist_ok=True)

    logger.info("Processing %s -> %s", image_path, run_dir)

    # Stage 1: load
    gray = io_utils.load_grayscale(image_path)
    io_utils.save_image(gray, run_dir / "01_original.png")

    # Stage 2: preprocess
    gaussian, clahe_img = preprocessing.preprocess(gray, cfg)
    if cfg.get("output", "save_intermediate", True):
        io_utils.save_image(gaussian, run_dir / "02_gaussian.png")
        io_utils.save_image(clahe_img, run_dir / "03_clahe.png")

    # Stage 3: edges (QC only, does not feed segmentation)
    edges = edge_detection.detect_edges(clahe_img, cfg)
    if cfg.get("output", "save_intermediate", True):
        io_utils.save_image(edges, run_dir / "04_edges.png")

    # Stage 4: segmentation
    binary, threshold_value = segmentation.segment(clahe_img, cfg)
    if cfg.get("output", "save_intermediate", True):
        io_utils.save_image(binary, run_dir / "05_threshold.png")
    logger.info("Segmentation method=%s threshold=%s", cfg.get("segmentation", "method"), threshold_value)

    # Stage 5: morphology cleanup
    clean = morphology_ops.clean_mask(binary, cfg)
    io_utils.save_image(clean, run_dir / "06_morphology.png")

    # Stage 6: connected components
    comps = components_mod.find_components(clean, cfg)
    comp_vis = visualization.draw_components(clean, comps)
    io_utils.save_image(comp_vis, run_dir / "07_components.png")
    logger.info("Detected %d component(s) above min_area threshold", len(comps))

    # Stage 7: numbering
    ordered = numbering.order_components(comps, cfg)
    numbered_vis = visualization.draw_numbered(clean, ordered)
    io_utils.save_image(numbered_vis, run_dir / "08_numbered.png")

    overlay_vis = None
    if cfg.get("output", "make_overlay_on_original", True):
        overlay_vis = visualization.overlay_on_original(gray, ordered)
        io_utils.save_image(overlay_vis, run_dir / "09_overlay_on_original.png")

    qc_vis = visualization.edge_qc_overlay(gray, edges, clean)
    io_utils.save_image(qc_vis, run_dir / "10_edge_qc_overlay.png")

    # Stage 8: optional metrics
    eval_metrics = None
    if ground_truth_path is not None and Path(ground_truth_path).exists():
        gt = io_utils.load_grayscale(ground_truth_path)
        eval_metrics = metrics.evaluate(clean, gt)
        logger.info("Evaluation vs ground truth: %s", eval_metrics)

    summary = {
        "image": str(image_path),
        "num_bones_detected": len(ordered),
        "threshold_value": threshold_value,
        "components": [
            {"number": i + 1, "area": c.area, "bbox": c.bbox, "centroid": c.centroid}
            for i, c in enumerate(ordered)
        ],
        "metrics": eval_metrics,
        "config": cfg.as_dict(),
    }
    with open(run_dir / "summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    if show:
        _show_results(gray, clean, numbered_vis, overlay_vis)

    return summary


def _show_results(gray, clean, numbered_vis, overlay_vis) -> None:
    """Optional interactive display. Only called when --show is passed;
    disabled by default so the pipeline runs headlessly (e.g. over SSH,
    in CI, or in batch mode) without blocking on a window."""
    import cv2  # local import: only needed in interactive mode

    cv2.imshow("Original", gray)
    cv2.imshow("Final Mask", clean)
    cv2.imshow("Numbered", numbered_vis)
    if overlay_vis is not None:
        cv2.imshow("Overlay on Original", overlay_vis)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
