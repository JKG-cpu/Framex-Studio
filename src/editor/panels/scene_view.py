# ===================================
# QWidget: QPainter Rendering + Input
# ===================================
from PySide6.QtWidgets import (
    QVBoxLayout, QLabel, QWidget
)
from PySide6.QtGui import (
    QPainter, QPen, QBrush, QColor, QFont
)
from PySide6.QtCore import Qt, QPointF

from ...runtime import BaseObject
from ..scene_editor import SceneEditor
from .base_panel import Panel

# Draw objects as rectangles
# Click to select
# Drag to move
# Swap rectangles for sprites

__all__ = ["SceneView"]

class SceneView(Panel):
    def __init__(self, scene_editor: SceneEditor, parent = None) -> None:
        super().__init__(parent)
        self.setObjectName("SceneView")
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.scene_editor = scene_editor

        # Pan + Zoom
        self.zoom = 5
        self.pan: QPointF = QPointF(0, 0)

    # Helpers
    #region
    def world_to_screen(self, world_pos: QPointF) -> QPointF:
        return (world_pos + self.pan) * self.zoom
    
    def screen_to_world(self, screen_pos: QPointF) -> QPointF:
        return (screen_pos / self.zoom) - self.pan
    #endregion

    # Mouse Events
    #region
    def wheelEvent(self, event) -> None:
        delta = event.angleDelta()

        if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            zoom_step = 0.5
            self.zoom += zoom_step if delta.y() > 0 else -zoom_step
            self.zoom = max(1, min(self.zoom, 10.0))
        else:
            self.pan += QPointF(-delta.x(), -delta.y()) * 0.5

        self.update()
    #endregion

    # Drawing
    #region
    def draw_grid(self, painter: QPainter) -> None:
        base_grid = 50
        scaled_grid = base_grid * self.zoom

        while scaled_grid < 20:
            scaled_grid *= 2

        while scaled_grid > 100:
            scaled_grid /= 2

        start_x = -(self.pan.x() % scaled_grid)
        start_y = -(self.pan.y() % scaled_grid)

        pen = QPen(QColor("#FFFFFF"), 1)
        painter.setPen(pen)

        x = start_x
        while x < self.width():
            painter.drawLine(int(x), 0, int(x), self.height())
            x += scaled_grid

        y = start_y
        while y < self.height():
            painter.drawLine(0, int(y), self.width(), int(y))
            y += scaled_grid

    def draw_object(self, painter: QPainter, obj: BaseObject) -> None:
        screen_pos = self.world_to_screen(obj.get_position())
        
        obj_size = obj.get_size()
        obj_scale = obj.scale()

        screen_w = obj_size.x() * obj_scale.x() * self.zoom
        screen_h = obj_size.y() * obj_scale.y() * self.zoom

        painter.drawRect(
            int(screen_pos.x()),
            int(screen_pos.y()),
            int(screen_w),
            int(screen_h)
        )

    def paintEvent(self, event):
        with QPainter(self) as painter:
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)

            pen = QPen(QColor("#FFFFFF"), 3, Qt.PenStyle.SolidLine)
            painter.setPen(pen)

            brush = QBrush(QColor("#FFFFFF"), Qt.BrushStyle.SolidPattern)
            painter.setBrush(brush)

            margin = 5
            clip_rect = self.rect().adjusted(margin, margin, -margin, -margin)
            painter.setClipRect(clip_rect)

            for obj in self.scene_editor.get_objects():
                self.draw_object(painter, obj)

            self.draw_grid(painter)

    #endregion