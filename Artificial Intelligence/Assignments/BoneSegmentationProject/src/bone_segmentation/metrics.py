"""
Stage 8 (optional): Quantitative evaluation.

The original project had no way to measure whether the segmentation was
actually any good - only qualitative eyeballing of saved PNGs. If a
ground-truth binary mask is available (same filename, placed in
dataset/ground_truth/), Dice and IoU are computed against the final
predicted mask.
"""

from __future__ import annotations

from typing import Dict

import numpy as np


def evaluate(pred_mask: np.ndarray, gt_mask: np.ndarray) -> Dict[str, float]:
    pred = (pred_mask > 0).astype(np.uint8)
    gt = (gt_mask > 0).astype(np.uint8)

    if pred.shape != gt.shape:
        raise ValueError(
            f"Prediction/ground-truth shape mismatch: {pred.shape} vs {gt.shape}"
        )

    intersection = int(np.logical_and(pred, gt).sum())
    union = int(np.logical_or(pred, gt).sum())
    pred_sum = int(pred.sum())
    gt_sum = int(gt.sum())

    dice = (2 * intersection) / (pred_sum + gt_sum) if (pred_sum + gt_sum) > 0 else 1.0
    iou = intersection / union if union > 0 else 1.0

    return {"dice": round(dice, 4), "iou": round(iou, 4)}
