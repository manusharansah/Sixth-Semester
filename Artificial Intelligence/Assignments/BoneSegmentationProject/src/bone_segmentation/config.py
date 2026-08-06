"""
Centralized, overridable configuration for the pipeline.

All the "magic numbers" that were previously scattered and hardcoded across
individual scripts (kernel sizes, thresholds, min area, etc.) live here.
Values can be overridden by editing config.yaml at the project root, or by
passing CLI flags to main.py (CLI flags win over the YAML file, which wins
over these defaults).
"""

from __future__ import annotations

import copy
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Dict

try:
    import yaml  # PyYAML
except ImportError:  # pragma: no cover
    yaml = None


DEFAULTS: Dict[str, Any] = {
    "preprocessing": {
        "gaussian_kernel": 5,       # odd int, blur strength
        "clahe_clip_limit": 2.0,    # contrast limiting for CLAHE
        "clahe_tile_grid": 8,       # NxN tile grid for CLAHE
    },
    "edge_detection": {
        "canny_low": 50,
        "canny_high": 150,
    },
    "segmentation": {
        "method": "otsu",           # "otsu" or "adaptive"
        "adaptive_block_size": 35,  # only used if method == "adaptive"
        "adaptive_c": 5,            # only used if method == "adaptive"
    },
    "morphology": {
        "kernel_size": 5,
        "min_area": 500,            # px^2, discard components smaller than this
        "fill_holes": True,
    },
    "components": {
        "use_watershed": False,     # attempt to split touching/overlapping bones
        "watershed_min_distance": 15,
    },
    "numbering": {
        # order bones left-to-right, top-to-bottom for reproducible numbering
        "sort_by": "reading_order",  # "reading_order" or "area_desc"
    },
    "output": {
        "save_intermediate": True,
        "make_overlay_on_original": True,
    },
}


@dataclass
class Config:
    data: Dict[str, Any] = field(default_factory=lambda: copy.deepcopy(DEFAULTS))

    @classmethod
    def load(cls, yaml_path: Path | None = None) -> "Config":
        cfg = copy.deepcopy(DEFAULTS)
        if yaml_path is not None and Path(yaml_path).exists():
            if yaml is None:
                raise RuntimeError(
                    "PyYAML is not installed but a config file was provided. "
                    "Run: pip install pyyaml"
                )
            with open(yaml_path, "r") as f:
                user_cfg = yaml.safe_load(f) or {}
            cfg = _deep_merge(cfg, user_cfg)
        return cls(data=cfg)

    def get(self, section: str, key: str, default: Any = None) -> Any:
        return self.data.get(section, {}).get(key, default)

    def as_dict(self) -> Dict[str, Any]:
        return copy.deepcopy(self.data)

    def override(self, section: str, key: str, value: Any) -> None:
        self.data.setdefault(section, {})[key] = value


def _deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    result = copy.deepcopy(base)
    for k, v in override.items():
        if isinstance(v, dict) and isinstance(result.get(k), dict):
            result[k] = _deep_merge(result[k], v)
        else:
            result[k] = v
    return result
