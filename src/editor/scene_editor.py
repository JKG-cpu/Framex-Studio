# ==========================
# Manages Current Open Scene
# ==========================
from pathlib import Path

from ..runtime import BaseObject
from ..serialization import *

__all__ = ["SceneEditor"]


class SceneEditor:
    def __init__(self) -> None:
        self.scene_parser = SceneParser()
        self.scene_path: Path | None = None
        self.scene_data: None | dict = None
        self.objects: list[BaseObject] = []

    def select_scene(self, path: Path) -> None:
        self.scene_path = path
        self.scene_data = self.scene_parser.parse_path(path)
        self.objects = self.scene_data["objects"]

    def save_scene(self, path: Path, data: dict) -> None:
        self.scene_parser.save_path(path, data)
