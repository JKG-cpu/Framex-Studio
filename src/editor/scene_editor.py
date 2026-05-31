# ==========================
# Manages Current Open Scene
# ==========================
from ..runtime import BaseObject

__all__ = ["SceneEditor"]

class SceneEditor:
    def __init__(self) -> None:
        self.scene = None
        self.objects: list[BaseObject] = [
            BaseObject()
        ]

    # Get
    #region
    def get_objects(self) -> list[BaseObject]: return self.objects
    #endregion
    