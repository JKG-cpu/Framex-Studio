# ===================================
# QWidget: QPainter Rendering + Input
# ===================================
from PySide6.QtWidgets import (
    QVBoxLayout, QLabel, QWidget, QPushButton, QFrame, QHBoxLayout
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
# Add some buttons (return to (0, 0), navbar?) => DONE (framework)
# Create Basic objects in runtime/game_object.py and components/
# Add Basic Objects to Scene View
# Select / Move Basic Objects

__all__ = ["SceneView"]

class SceneView(Panel):
    def __init__(self, item_colors: dict[str, str], parent = None) -> None:
        super().__init__(parent)
        self.item_colors: dict[str, str] = item_colors

        self.setObjectName("SceneView")
        self.setStyleSheet(self.styleSheet() + f"background: {self.item_colors["background"]}; color: {self.item_colors["text"]}")

        # Pan / Zoom
        self.zoom: float = 1.0
        self.snap: float = 50.0
        self.pan: QPointF = QPointF(50.0, 50.0)

        self._setup_bars()

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
    
    def _setup_bars(self) -> None:
        self.top_bar = QFrame(self)
        self.top_bar.setFixedHeight(32)
        self.top_bar.setObjectName("SceneviewTopBar")
        self.top_bar.setStyleSheet("#SceneviewTopBar { border: 1px solid white; } color: white; background: transparent;")

        top_layout = QHBoxLayout(self.top_bar)
        top_layout.setContentsMargins(10, 4, 10, 4)

        top_layout.addStretch()
        top_layout.addWidget(QLabel("Scene View"))
        top_layout.addStretch()

        self.edit_bar = QFrame(self)
        self.edit_bar.setFixedHeight(32)
        self.edit_bar.setObjectName("SceneviewEditBar")
        self.edit_bar.setStyleSheet("#SceneviewEditBar { border: 1px solid white; } color: white; background: transparent;")
        
        edit_layout = QHBoxLayout(self.edit_bar)
        edit_layout.setContentsMargins(10, 4, 10, 4)

        play_button = QPushButton("▶️")
        play_button.clicked.connect(self._play)

        pause_button = QPushButton("⏸️")

        edit_layout.addStretch()
        edit_layout.addWidget(play_button)
        edit_layout.addStretch()

        self.bottom_bar = QFrame(self)
        self.bottom_bar.setFixedHeight(32)
        self.bottom_bar.setObjectName("SceneviewBottomBar")
        self.bottom_bar.setStyleSheet("#SceneviewBottomBar { border: 1px solid white; } color: white; background: transparent;")

        bottom_layout = QHBoxLayout(self.bottom_bar)
        bottom_layout.setContentsMargins(10, 4, 10, 4)

        rto_button = QPushButton("Return to (0, 0)")
        rto_button.clicked.connect(self._rto_button)

        bottom_layout.addStretch()
        bottom_layout.addWidget(rto_button)
    #endregion

    # Widget Events
    #region
    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        base_margin = 20

        self.top_bar.adjustSize()
        self.top_bar.move(
            (self.width() // 2) - (self.top_bar.width() // 2) - base_margin,
            base_margin + 15
        )

        self.edit_bar.adjustSize()
        self.edit_bar.move(
            self.width() - self.edit_bar.width() - base_margin,
            base_margin + 15
        )

        self.bottom_bar.adjustSize()
        self.bottom_bar.move(self.width() - self.bottom_bar.width() - base_margin, self.height() - self.bottom_bar.height() - base_margin)

    def _rto_button(self) -> None: 
        self.pan = QPointF(50.0, 50.0)
        self.update()

    def _play(self) -> None:
        # Compile (?) and play
        pass

    def _edit(self) -> None:
        pass
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
        top_left_world = self.screen_to_world(QPointF(0, 0))
        bottom_right_world = self.screen_to_world(QPointF(self.width(), self.height()))

        # Snap the start world positions to the nearest lower step of 50
        start_world_x = (top_left_world.x() // self.snap) * self.snap
        end_world_x = (bottom_right_world.x() // self.snap) * self.snap + self.snap

        start_world_y = (top_left_world.y() // self.snap) * self.snap
        end_world_y = (bottom_right_world.y() // self.snap) * self.snap + self.snap

        painter.setPen(QPen(QColor(self.item_colors["x_axis"])))

        world_x = start_world_x
        while world_x <= end_world_x:
            screen_x = (world_x + self.pan.x()) * self.zoom
            painter.drawLine(int(screen_x), 0, int(screen_x), self.height())
            world_x += self.snap
        
        painter.setPen(QPen(QColor(self.item_colors["y_axis"])))

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
        painter.setPen(QPen(QColor(self.item_colors["coord_text"])))

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
        painter.setPen(QPen(QColor(self.item_colors["origin"]), 2))
        painter.drawLine(x - size, y, x + size, y)
        painter.drawLine(x, y - size, x, y + size)

        # "0,0" label
        painter.setFont(QFont("Arial", 8))
        painter.setPen(QPen(QColor(self.item_colors["origin"])))
        painter.drawText(x + 6, y - 4, "0, 0")

    def paintEvent(self, event) -> None:
        with QPainter(self) as painter:
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)

            margin = 7
            clip_rect = self.rect().adjusted(margin, margin - 1, -margin, -margin)
            painter.setClipRect(clip_rect)

            # Background
            painter.fillRect(self.rect(), self.item_colors["background"])

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
