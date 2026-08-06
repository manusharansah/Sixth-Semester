# Bone Segmentation Pipeline (v2)

A classical computer-vision pipeline (OpenCV / scikit-image, **no deep
learning**) that takes a grayscale X-ray image, segments the bone regions,
and numbers each detected bone. This is a rebuilt version of an earlier
prototype project — same goal, same overall approach, but restructured
into a real, runnable, testable Python project.

## What this project does

Given an X-ray image, the pipeline:

1. **Loads** the image
2. **Preprocesses** it (Gaussian denoising + CLAHE contrast enhancement)
3. **Computes a Canny edge map** (kept as a diagnostic/QC overlay — see note below)
4. **Segments** bone vs. background (Otsu or adaptive thresholding)
5. **Cleans up** the mask (morphological opening/closing, hole filling, small-object removal)
6. **Finds connected components** (each blob = one candidate bone: bounding box + centroid)
7. **Numbers** the bones in a stable, human-readable order (top-to-bottom, left-to-right) and draws the numbers both on the mask and on the original image
8. **Optionally scores** the result against a ground-truth mask (Dice / IoU), if you have one

Every stage's intermediate image is saved to disk, and a `summary.json`
with all measurements is written per image.

## What changed from the original prototype, and why

The original project was a good first draft but had a number of practical
problems that made it hard to actually run, extend, or trust. This version
keeps the exact same goal and approach (classical CV bone segmentation +
numbering) and fixes the following:

| #  | Problem in the original project                                                                                                                                                                      | Fix in this version                                                                                                                                                                                       |
| -- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1  | `requirement.txt` (wrong filename) was **empty** — no way to actually install dependencies                                                                                                  | `requirements.txt` with pinned, tested versions                                                                                                                                                         |
| 2  | `main.py` was **empty** — you had to run 7 separate scripts by hand, in the right order                                                                                                     | Single`main.py` CLI that runs the whole pipeline (or individual stages)                                                                                                                                 |
| 3  | Every script hardcoded paths like`"../dataset/image1.png"`, so it only worked if you `cd`'d into `src/` first                                                                                  | `pathlib`-based paths resolved relative to the project root, and passed via CLI arguments                                                                                                               |
| 4  | Every script called`cv2.imshow()` + `cv2.waitKey(0)`, which **blocks and requires a display** — fails over SSH, in CI, on headless servers                                                | Headless by default; interactive display is opt-in via`--show`                                                                                                                                          |
| 5  | Only ever processed a single hardcoded image (`image1.png`)                                                                                                                                        | Supports a single`--image` or a whole `--image-dir` (batch mode)                                                                                                                                      |
| 6  | The Canny edge detection step computed an edge map that was**never used by anything downstream** — dead code                                                                                  | Kept, but explicitly repositioned as a diagnostic QC overlay (`10_edge_qc_overlay.png`) that shows how well the segmentation boundary tracks real intensity edges — documented, not silently discarded |
| 7  | Bones were numbered in whatever arbitrary order`connectedComponentsWithStats` returned labels in — not reproducible or intuitive                                                                  | Bones are sorted into reading order (top-to-bottom, left-to-right) before numbering, configurable to sort by area instead                                                                                 |
| 8  | No handling for touching/overlapping bones — thresholding + morphology alone can merge two adjacent bones into a single blob                                                                        | Optional watershed-based splitting (`--watershed` flag / `components.use_watershed` in config)                                                                                                        |
| 9  | No way to measure whether the segmentation was actually*good* — only eyeballing PNGs                                                                                                              | Optional Dice / IoU evaluation against a ground-truth mask                                                                                                                                                |
| 10 | `print()` statements everywhere, no persistent log                                                                                                                                                 | Proper`logging` module output to console **and** `outputs/run.log`                                                                                                                              |
| 11 | Magic numbers (kernel sizes, thresholds, min area, CLAHE params) scattered and duplicated across every script                                                                                        | Centralized, documented`config.yaml`, overridable per-run via CLI flags                                                                                                                                 |
| 12 | Scripts named`01_read_image.py`, `02_preprocessing.py`, etc. — filenames starting with a digit **cannot be imported** as Python modules, so the code could never be reused or unit tested | Proper installable package`src/bone_segmentation/` with descriptive, importable module names                                                                                                            |
| 13 | No tests at all                                                                                                                                                                                      | `tests/test_pipeline.py` (pytest) — smoke tests for loading, the full pipeline, both threshold methods, and the metrics module                                                                         |
| 14 | No error handling beyond`print(...); exit()`                                                                                                                                                       | Custom`ImageLoadError`, proper exceptions, and batch mode skips and logs failures instead of crashing the whole run                                                                                     |
| 15 | Outputs from every run overwrote the same 8 files in`outputs/`, no per-image organization                                                                                                          | Each run writes to`outputs/<image_name>/`, so batch runs and repeat experiments don't clobber each other                                                                                                |
| 16 | Only a mask-only visualization — hard to judge results against real anatomy                                                                                                                         | Added an overlay of the numbered bones drawn directly on the original image (`09_overlay_on_original.png`)                                                                                              |
| 17 | The shipped zip included a full Windows`venv/` folder (hundreds of MB of compiled `matplotlib`/etc.) plus macOS `__MACOSX/` and `.DS_Store` junk                                             | `.gitignore` excludes `venv/`, caches, and OS junk; you build your own virtual environment locally (see below)                                                                                        |
| 18 | No documentation of parameters or limitations                                                                                                                                                        | This README, inline docstrings, and comments in`config.yaml`                                                                                                                                            |

**Not changed:** the core goal (classical, explainable CV pipeline that
segments and numbers bones in an X-ray) and the overall stage order. This
is a re-engineering pass, not a redesign.

## Project structure

```
BoneSegmentationProject/
├── README.md
├── requirements.txt
├── config.yaml                 # all tunable parameters, documented
├── main.py                     # CLI entry point — run this
├── .gitignore
├── dataset/
│   ├── image1.png              # bundled sample X-ray image
│   └── ground_truth/           # (optional) put ground-truth masks here for evaluation
├── outputs/                    # generated results land here (git-ignored except .gitkeep)
├── src/
│   └── bone_segmentation/      # the actual importable/testable package
│       ├── __init__.py
│       ├── config.py           # Config dataclass + defaults + YAML loading
│       ├── logger_utils.py     # logging setup
│       ├── io_utils.py         # image load/save with real error handling
│       ├── preprocessing.py    # Gaussian blur + CLAHE
│       ├── edge_detection.py   # Canny (QC only)
│       ├── segmentation.py     # Otsu / adaptive thresholding
│       ├── morphology_ops.py   # open/close/fill-holes/remove-small-objects
│       ├── components.py       # connected components (+ optional watershed)
│       ├── numbering.py        # spatial ordering for reproducible numbering
│       ├── visualization.py    # all drawing/overlay code
│       ├── metrics.py          # Dice / IoU evaluation
│       └── pipeline.py         # orchestrates all stages for one image
└── tests/
    └── test_pipeline.py        # pytest smoke tests
```

## Prerequisites

- Python 3.9–3.12 (developed/tested on 3.12)
- pip

## Setup (run these on your laptop)

```bash
# 1. Unzip and enter the project folder
cd BoneSegmentationProject

# 2. Create and activate a virtual environment
python3 -m venv venv

# macOS/Linux:
source venv/bin/activate
# Windows (PowerShell):
venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install unpinned/latest versions
pip install --upgrade opencv-python numpy scipy scikit-image PyYAML pytest
```

> **Note on OpenCV variants:** `requirements.txt` installs `opencv-python`,
> which includes GUI support (needed for `--show`). If you only ever plan
> to run headlessly (no `--show`), you can swap it for the smaller
> `opencv-python-headless` instead.

## Running the pipeline

Run on the bundled sample image:

```bash
python main.py --image dataset/image1.png
```

Run on every image in a folder (batch mode):

```bash
python main.py --image-dir dataset/
```

Show results interactively in OpenCV windows (press any key to close):

```bash
python main.py --image dataset/image1.png --show
```

Use adaptive thresholding instead of Otsu:

```bash
python main.py --image dataset/image1.png --seg-method adaptive
```

Try to split bones that are touching/overlapping (watershed):

```bash
python main.py --image dataset/image1.png --watershed
```

Change any parameter without touching code — edit `config.yaml`, or override on the CLI:

```bash
python main.py --image dataset/image1.png --min-area 300
```

Evaluate against a ground-truth mask:

```bash
# put a same-named binary mask PNG in dataset/ground_truth/, e.g. dataset/ground_truth/image1.png
python main.py --image dataset/image1.png --ground-truth dataset/ground_truth/image1.png
```

See all options:

```bash
python main.py --help
```

## Where to look at results

For each processed image, a folder `outputs/<image_name>/` is created containing:

| File                           | What it shows                                                                                                                                    |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| `01_original.png`            | Grayscale input                                                                                                                                  |
| `02_gaussian.png`            | After denoising                                                                                                                                  |
| `03_clahe.png`               | After contrast enhancement                                                                                                                       |
| `04_edges.png`               | Canny edge map (diagnostic)                                                                                                                      |
| `05_threshold.png`           | Raw binary segmentation                                                                                                                          |
| `06_morphology.png`          | Cleaned-up final mask                                                                                                                            |
| `07_components.png`          | Detected components with bounding boxes + centroids                                                                                              |
| `08_numbered.png`            | Numbered bones drawn on the mask                                                                                                                 |
| `09_overlay_on_original.png` | Numbered bones drawn on the**original** image                                                                                              |
| `10_edge_qc_overlay.png`     | Canny edges (red) vs. final mask boundary (green), for sanity-checking segmentation quality                                                      |
| `summary.json`               | Machine-readable results: bone count, bounding boxes, centroids, threshold value used, config used, and metrics (if a ground truth was supplied) |

A run-level log is also written to `outputs/run.log`.

## Running the tests

```bash
pytest -v
```

This runs smoke tests that check: the sample image loads, missing files
raise a clear error instead of crashing silently, the full pipeline runs
end-to-end and produces every expected output file, both threshold methods
work, and the Dice/IoU metric is correct on known cases.

## Using your own X-ray images

Drop any grayscale (or color — it will be converted) image into `dataset/`
and run `python main.py --image dataset/your_file.png`, or point
`--image-dir` at a folder containing several images for batch processing.
Supported formats: PNG, JPG/JPEG, BMP, TIF/TIFF.

## Known limitations & possible future work

This remains a **classical image-processing** pipeline, not a trained
segmentation model — it is intentionally simple, fast, and fully
explainable, but that comes with real limits worth knowing:

- **Threshold-based segmentation is intensity-dependent.** It works well
  when bone is clearly brighter than surrounding soft tissue, but can
  under/over-segment on low-contrast or unevenly-exposed X-rays. Try
  `--seg-method adaptive` on images where a single global threshold
  (Otsu) doesn't work well.
- **Touching/overlapping bones can still merge** into one component even
  with `--watershed` enabled if they overlap heavily — watershed helps but
  is not guaranteed to correctly separate every case.
- **No learned anatomical prior.** The pipeline has no notion of "this
  blob is a femur" vs. "this blob is a tibia" — it only numbers bones by
  position, it does not classify them.
- **A trained segmentation model (e.g., U-Net) would generally outperform
  this approach** on harder images, at the cost of needing labeled
  training data, GPU resources, and losing some of the interpretability of
  a classical pipeline. That would be a legitimate next step but is out of
  scope here, since it changes the project from "classical CV pipeline"
  to "ML model" — this rebuild deliberately preserves the original
  project's scope and approach.

## License / data note

The bundled `dataset/image1.png` is the same sample image used in the
original prototype project, included only for demonstration/testing
purposes. Replace it with your own licensed/consented imaging data for
any real use.
