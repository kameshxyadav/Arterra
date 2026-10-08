"""Feature schema placeholder for Phase 2.

The real implementation will read `config/features.yaml` and expose a convenient
Python object (e.g. a Pydantic model or a simple dataclass) that lists all
available feature keys, types, and any defaults. For now we provide a minimal
`Schema` class that loads the YAML file into a dictionary and offers a few
helper methods.
"""

import pathlib
import yaml
from typing import Dict, List, Any

CONFIG_PATH = pathlib.Path(__file__).resolve().parents[2] / "config" / "features.yaml"


class Schema:
    """Simple container for the feature configuration.

    Attributes
    ----------
    raw : dict
        The raw parsed YAML content.
    groups : dict
        Mapping of group name → list of feature dictionaries.
    """

    def __init__(self, config_path: pathlib.Path | None = None):
        self.path = pathlib.Path(config_path) if config_path else CONFIG_PATH
        if not self.path.exists():
            raise FileNotFoundError(f"Features config not found: {self.path}")
        with open(self.path, "r", encoding="utf-8") as f:
            self.raw: Dict[str, Any] = yaml.safe_load(f) or {}
        self.groups = self.raw.get("groups", {})

    def feature_keys(self) -> List[str]:
        """Return a flat list of all feature `name` entries across groups."""
        keys: List[str] = []
        for feats in self.groups.values():
            for feat in feats:
                if "name" in feat:
                    keys.append(feat["name"])
        return keys

    def get_feature(self, name: str) -> Dict[str, Any] | None:
        """Return the feature dict for `name` or ``None`` if not present."""
        for feats in self.groups.values():
            for feat in feats:
                if feat.get("name") == name:
                    return feat
        return None

    def __repr__(self) -> str:
        return f"Schema(groups={list(self.groups.keys())}, total_features={len(self.feature_keys())})"
