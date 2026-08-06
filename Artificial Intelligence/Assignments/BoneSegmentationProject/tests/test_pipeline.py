"""
Smoke tests for the bone segmentation pipeline.

Run with:  pytest -v
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

import numpy as np
import pytest

from bone_segmentation.config import Config
from bone_segmentation.io_utils import ImageLoadError, load_grayscale
from bone_segmentation.logger_utils import get_logger
from bone_segmentation.metrics import evaluate
from bone_segmentation.pipeline import run_pipeline

SAMPLE_IMAGE = PROJECT_ROOT / "dataset" / "image1.png"


@pytest.fixture
def cfg():
    return Config.load(None)


@pytest.fixture
def logger():
    return get_logger("test")


def test_sample_image_present():
    assert SAMPLE_IMAGE.exists(), "Bundled sample image is missing"


def test_load_grayscale_success():
    img = load_grayscale(SAMPLE_IMAGE)
    assert img.ndim == 2
    assert img.shape[0] > 0 and img.shape[1] > 0


def test_load_grayscale_missing_file_raises():
    with pytest.raises(ImageLoadError):
        load_grayscale(PROJECT_ROOT / "dataset" / "does_not_exist.png")


def test_pipeline_runs_end_to_end(tmp_path, cfg, logger):
    summary = run_pipeline(SAMPLE_IMAGE, tmp_path, cfg, logger)

    run_dir = tmp_path / SAMPLE_IMAGE.stem
    expected_files = [
        "01_original.png", "05_threshold.png", "06_morphology.png",
        "07_components.png", "08_numbered.png", "09_overlay_on_original.png",
        "10_edge_qc_overlay.png", "summary.json",
    ]
    for fname in expected_files:
        assert (run_dir / fname).exists(), f"Missing expected output: {fname}"

    assert summary["num_bones_detected"] >= 0
    assert "components" in summary


def test_pipeline_with_adaptive_threshold(tmp_path, cfg, logger):
    cfg.override("segmentation", "method", "adaptive")
    summary = run_pipeline(SAMPLE_IMAGE, tmp_path, cfg, logger)
    assert summary["threshold_value"] == -1.0  # adaptive has no single global threshold


def test_metrics_perfect_match():
    mask = np.zeros((50, 50), dtype=np.uint8)
    mask[10:30, 10:30] = 255
    result = evaluate(mask, mask)
    assert result["dice"] == 1.0
    assert result["iou"] == 1.0


def test_metrics_no_overlap():
    a = np.zeros((50, 50), dtype=np.uint8)
    a[0:10, 0:10] = 255
    b = np.zeros((50, 50), dtype=np.uint8)
    b[40:50, 40:50] = 255
    result = evaluate(a, b)
    assert result["dice"] == 0.0
    assert result["iou"] == 0.0
