# ===================
# Transform Component
# ===================
from PySide6.QtCore import QPointF

__all__ = ["Transform"]

class Transform:
    def __init__(self) -> None:
        self.position: QPointF = QPointF(0, 0)
        self.rotation: float = 0.0
        self.scale: QPointF = QPointF(1, 1)
        self.size: QPointF = QPointF(50, 50)
        