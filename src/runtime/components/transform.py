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
    
    def to_dict(self) -> dict:
        return {
            "position": [self.position.x(), self.position.y()],
            "rotation": self.rotation,
            "scale": [self.scale.x(), self.scale.y()],
            "size": [self.size.x(), self.size.y()]
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Transform":
        t = cls()
        t.position = QPointF(*data["position"])
        t.rotation = data["rotation"]
        t.scale = QPointF(*data["scale"])
        t.size = QPointF(*data["size"])
        return t