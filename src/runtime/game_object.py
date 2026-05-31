# ================
# GameObject Class
# ================
from PySide6.QtCore import QPointF

from .components import *

__all__ = ["BaseObject"]

class BaseObject:
    def __init__(self) -> None:
        self.transform = Transform()

    # Set
    #region
    def set_position(self, x: float, y: float) -> None: self.transform.size = QPointF(x, y)
    #endregion

    # Get
    #region
    def get_position(self) -> QPointF: return self.transform.position
    def get_size(self) -> QPointF: return self.transform.size
    def scale(self) -> QPointF: return self.transform.scale
    #endregion
