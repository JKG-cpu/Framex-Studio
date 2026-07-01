# ====================
# Save/Load .scene JSON
# ====================
from pathlib import Path
from json import load, dump

from ..runtime import BaseObject

__all__ = ["SceneParser"]


class SceneParser:
    def parse_path(self, path: Path) -> dict:
        with open(path, "r") as f:
            d = load(f)

        d["objects"] = [BaseObject.from_dict(o) for o in d["objects"]]

        return d

    def save_path(self, path: Path, data: dict) -> None:
        data["objects"] = [obj.to_dict() for obj in data["objects"]]

        with open(path, "w") as f:
            dump(data, f, indent=2)
