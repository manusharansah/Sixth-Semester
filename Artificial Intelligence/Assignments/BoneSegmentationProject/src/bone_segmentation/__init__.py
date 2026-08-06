"""
bone_segmentation
==================

A classical (non-deep-learning) image processing pipeline for segmenting
and numbering bone regions in grayscale X-ray images using OpenCV.

Pipeline stages
---------------
1. Load          - read a grayscale image from disk
2. Preprocess     - Gaussian denoising + CLAHE contrast enhancement
3. Edge (QC)      - Canny edge map, used only as a diagnostic overlay
4. Segment        - Otsu / adaptive thresholding to a binary mask
5. Morphology     - opening + closing + small-object removal
6. Components     - connected-component analysis (bounding boxes, centroids)
7. Numbering      - spatially-ordered labeling and annotated overlay
8. Metrics (opt.) - Dice / IoU against a ground-truth mask, if supplied

See README.md for full usage instructions.
"""

from .pipeline import run_pipeline

__all__ = ["run_pipeline"]
__version__ = "2.0.0"
