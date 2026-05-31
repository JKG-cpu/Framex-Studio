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

# Create a Grid (View) => DONE
# Include Numbers (positions) on the grid => DONE
# Add Panning => DONE
# Create Basic objects in runtime/game_object.py and components/
# Add Basic Objects
# Select / Move Basic Objects

__all__ = ["SceneView"]

class SceneView(Panel):
    def __init__(self, parent = None) -> None:
        super().__init__(parent)
        self.setObjectName("SceneView")
    
        # Pan / Zoom
        self.zoom: float = 1.0
        self.snap: float = 50.0
        self.pan: QPointF = QPointF(50.0, 50.0)

    # Helpers
    #region
    def world_to_screen(self, world_pos: QPointF) -> QPointF: 
        return (world_pos + self.pan) * self.zoom
        
    def screen_to_world(self, screen_pos: QPointF, snap: bool = False) -> QPointF: 
        world_pos = (screen_pos / self.zoom) - self.pan
        
        if snap and self.snap > 0:
            snapped_x = round(world_pos.x() / self.snap) * self.snap
            snapped_y = round(world_pos.y() / self.snap) * self.snap
            return QPointF(snapped_x, snapped_y)
            
        return world_pos
    #endregion

    # Mouse Events
    #region
    def wheelEvent(self, event) -> None:
        delta = event.angleDelta()
        
        # Multiplier so you don't have to scroll forever
        pan_speed_multiplier = 2.0 
        
        self.pan += QPointF(
            delta.x() * pan_speed_multiplier, 
            delta.y() * pan_speed_multiplier
        )
        self.update()
    #endregion

    # Drawing
    #region
    def draw_grid(self, painter: QPainter) -> None:
        pen = QPen(QColor("#095496"), 1)
        painter.setPen(pen)

        top_left_world = self.screen_to_world(QPointF(0, 0))
        bottom_right_world = self.screen_to_world(QPointF(self.width(), self.height()))

        # Snap the start world positions to the nearest lower step of 50
        start_world_x = (top_left_world.x() // self.snap) * self.snap
        end_world_x = (bottom_right_world.x() // self.snap) * self.snap + self.snap

        start_world_y = (top_left_world.y() // self.snap) * self.snap
        end_world_y = (bottom_right_world.y() // self.snap) * self.snap + self.snap

        world_x = start_world_x
        while world_x <= end_world_x:
            screen_x = (world_x + self.pan.x()) * self.zoom
            painter.drawLine(int(screen_x), 0, int(screen_x), self.height())
            world_x += self.snap
        
        world_y = start_world_y
        while world_y <= end_world_y:
            screen_y = (world_y + self.pan.y()) * self.zoom
            painter.drawLine(0, int(screen_y), self.width(), int(screen_y))
            world_y += self.snap

    def draw_coords(self, painter: QPainter) -> None:
        scaled_grid = self.snap * self.zoom
        if scaled_grid < 40:
            return

        font = QFont("Arial", 8)
        painter.setFont(font)
        painter.setPen(QPen(QColor("#4a90b8")))

        top_left_world = self.screen_to_world(QPointF(0, 0))
        bottom_right_world = self.screen_to_world(QPointF(self.width(), self.height()))

        start_world_x = (top_left_world.x() // self.snap) * self.snap
        end_world_x = (bottom_right_world.x() // self.snap) * self.snap + self.snap

        start_world_y = (top_left_world.y() // self.snap) * self.snap
        end_world_y = (bottom_right_world.y() // self.snap) * self.snap + self.snap

        # Draw X-axis coordinate text numbers
        world_x = start_world_x
        while world_x <= end_world_x:
            if int(world_x) != 0:
                screen_x = (world_x + self.pan.x()) * self.zoom
                if screen_x > 20:
                    painter.drawText(int(screen_x) + 3, 14, str(int(world_x)))
            world_x += self.snap
        
        # Draw Y-axis coordinate text numbers
        world_y = start_world_y
        while world_y <= end_world_y:
            if int(world_y) != 0:
                screen_y = (world_y + self.pan.y()) * self.zoom
                if screen_y > 20:
                    painter.drawText(4, int(screen_y) - 3, str(int(world_y)))
            world_y += self.snap
        
    def draw_origin(self, painter: QPainter) -> None:
        origin_screen = self.world_to_screen(QPointF(0, 0))
        x, y = int(origin_screen.x()), int(origin_screen.y())

        size = 8
        painter.setPen(QPen(QColor("#ff4444"), 2))
        painter.drawLine(x - size, y, x + size, y)
        painter.drawLine(x, y - size, x, y + size)

        # "0,0" label
        painter.setFont(QFont("Arial", 8))
        painter.setPen(QPen(QColor("#ff4444")))
        painter.drawText(x + 6, y - 4, "0, 0")

    def paintEvent(self, event) -> None:
        with QPainter(self) as painter:
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)

            margin = 5
            clip_rect = self.rect().adjusted(margin, margin, -margin, -margin)
            painter.setClipRect(clip_rect)

            self.draw_grid(
                painter = painter
            )
            self.draw_coords(
                painter = painter
            )
            self.draw_origin(
                painter = painter
            )
    #endregion
