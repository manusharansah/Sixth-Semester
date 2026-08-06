#!/usr/bin/env python3
"""
CLI entry point for the bone segmentation pipeline.

Examples
--------
Run on the bundled sample image:
    python main.py --image dataset/image1.png

Run on every image in a folder (batch mode):
    python main.py --image-dir dataset/

Run with a config file and adaptive thresholding override:
    python main.py --image dataset/image1.png --config config.yaml --seg-method adaptive

Evaluate against a ground-truth mask (same filename in dataset/ground_truth/):
    python main.py --image dataset/image1.png --ground-truth dataset/ground_truth/image1.png

Show results interactively (opens OpenCV windows, waits for a keypress):
    python main.py --image dataset/image1.png --show
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from bone_segmentation.config import Config  # noqa: E402
from bone_segmentation.io_utils import list_images, ImageLoadError  # noqa: E402
from bone_segmentation.logger_utils import get_logger  # noqa: E402
from bone_segmentation.pipeline import run_pipeline  # noqa: E402


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Bone segmentation & numbering pipeline")
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("--image", type=str, help="Path to a single input image")
    src.add_argument("--image-dir", type=str, help="Path to a folder of images (batch mode)")

    p.add_argument("--output", type=str, default="outputs", help="Output root directory (default: outputs)")
    p.add_argument("--config", type=str, default="config.yaml", help="Path to config.yaml (optional)")
    p.add_argument("--ground-truth", type=str, default=None,
                    help="Path to a ground-truth mask (single-image mode only)")
    p.add_argument("--ground-truth-dir", type=str, default=None,
                    help="Folder of ground-truth masks matching filenames in --image-dir")
    p.add_argument("--show", action="store_true", help="Display results in OpenCV windows (blocks on keypress)")

    p.add_argument("--seg-method", choices=["otsu", "adaptive"], default=None,
                    help="Override segmentation.method from config")
    p.add_argument("--min-area", type=int, default=None,
                    help="Override morphology.min_area from config")
    p.add_argument("--watershed", action="store_true",
                    help="Enable watershed splitting of touching components")

    p.add_argument("--log-file", type=str, default="outputs/run.log", help="Path to write log output")
    return p


def main() -> int:
    args = build_arg_parser().parse_args()

    cfg_path = Path(args.config)
    cfg = Config.load(cfg_path if cfg_path.exists() else None)

    if args.seg_method:
        cfg.override("segmentation", "method", args.seg_method)
    if args.min_area is not None:
        cfg.override("morphology", "min_area", args.min_area)
    if args.watershed:
        cfg.override("components", "use_watershed", True)

    output_dir = Path(args.output)
    logger = get_logger(log_file=Path(args.log_file))

    try:
        if args.image:
            image_path = Path(args.image)
            gt_path = Path(args.ground_truth) if args.ground_truth else None
            run_pipeline(image_path, output_dir, cfg, logger, ground_truth_path=gt_path, show=args.show)
        else:
            image_dir = Path(args.image_dir)
            images = list_images(image_dir)
            logger.info("Batch mode: found %d image(s) in %s", len(images), image_dir)
            failures = []
            for img_path in images:
                gt_path = None
                if args.ground_truth_dir:
                    candidate = Path(args.ground_truth_dir) / img_path.name
                    gt_path = candidate if candidate.exists() else None
                try:
                    run_pipeline(img_path, output_dir, cfg, logger, ground_truth_path=gt_path, show=args.show)
                except ImageLoadError as e:
                    logger.error("Skipping %s: %s", img_path, e)
                    failures.append(str(img_path))
            if failures:
                logger.warning("Completed with %d failure(s): %s", len(failures), failures)
    except (ImageLoadError, FileNotFoundError) as e:
        logger.error(str(e))
        return 1

    logger.info("Done. Results written under: %s", output_dir.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
