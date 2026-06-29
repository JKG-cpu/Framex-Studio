# ===================================
# QWidget: QPainter Rendering + Input
# ===================================
from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout,
    QLabel, QWidget, QPushButton, QFrame,
    QApplication, QStyle
)
from PySide6.QtGui import (
    QPainter, QPen, QBrush, QColor, QFont, QKeyEvent, QMouseEvent
)
from PySide6.QtCore import Qt, QPointF, Signal

from ...runtime import BaseObject
from ..scene_editor import SceneEditor
from .base_panel import Panel

__all__ = ["SceneView"]

class SceneView(Panel):
    save_scene = Signal(dict)

    def __init__(self, theme: dict[str, str], scene = None, parent = None) -> None:
        super().__init__(parent)
        self.theme: dict[str, str] = theme

        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.setMouseTracking(True)
        self.setObjectName("SceneView")

        # Icons
        style = QApplication.style()
        self.start_icon = style.standardIcon(QStyle.SP_MediaPlay)
        self.pause_icon = style.standardIcon(QStyle.SP_MediaPause)
        self.stop_icon  = style.standardIcon(QStyle.SP_MediaStop)

        # Pan / Zoom
        self.zoom: float = 1.0
        self.snap: float = 50.0
        self.pan: QPointF = QPointF(50.0, 50.0)

        # Selection
        self.allow_snap: bool = False
        self.selected_object: BaseObject | None = None
        self.drag_offset: QPointF = QPointF(0, 0)

        self._setup_bars()

        self.scene: dict | None = scene
        self.objects: list[BaseObject] = self._load_scene_objects()

    # Scene Handling
    #region
    def select_scene(self, scene: dict) -> None:
        if scene is self.scene:
            self.update()
            return

        self.scene = scene
        self.objects = self._load_scene_objects()
        self.update()

    def _load_scene_objects(self) -> None:
        return self.scene.get("objects", []) if self.scene else []

    def _save_scene(self) -> None:
        self.save_scene.emit(self.scene)
    #endregion

    # Helpers
    #region
    def world_to_screen(self, world_pos: QPointF) -> QPointF:  return (world_pos + self.pan) * self.zoom
    def screen_to_world(self, screen_pos: QPointF) -> QPointF: return (screen_pos / self.zoom) - self.pan
    
    def _setup_bars(self) -> None:
        self.top_bar = QFrame(self)
        self.top_bar.setFixedHeight(32)
        self.top_bar.setObjectName("SceneviewTopBar")
        
        top_layout = QHBoxLayout(self.top_bar)
        top_layout.setContentsMargins(10, 4, 10, 4)

        top_layout.addStretch()
        top_layout.addWidget(QLabel("Scene View"))
        top_layout.addStretch()

        self.edit_bar = QFrame(self)
        self.edit_bar.setFixedHeight(32)
        self.edit_bar.setObjectName("SceneviewEditBar")
        
        edit_layout = QHBoxLayout(self.edit_bar)
        edit_layout.setContentsMargins(10, 4, 10, 4)
        edit_layout.setSpacing(4)

        play_button = QPushButton()
        play_button.setIcon(self.start_icon)
        play_button.clicked.connect(self._play)

        pause_button = QPushButton()
        pause_button.setIcon(self.pause_icon)

        edit_layout.addStretch()
        edit_layout.addWidget(play_button)
        edit_layout.addStretch()

        self.bottom_bar = QFrame(self)
        self.bottom_bar.setFixedHeight(32)
        self.bottom_bar.setObjectName("SceneviewBottomBar")
        
        bottom_layout = QHBoxLayout(self.bottom_bar)
        bottom_layout.setContentsMargins(10, 4, 10, 4)

        rto_button = QPushButton("Return to (0, 0)")
        rto_button.clicked.connect(self._rto_button)

        bottom_layout.addStretch()
        bottom_layout.addWidget(rto_button)
    
    def get_object_at(self, world_pos: QPointF) -> BaseObject | None:
        for obj in self.objects:
            x, y = obj.position.x(), obj.position.y()
            w, h = obj.size.x() * obj.scale.x(), obj.size.y() * obj.scale.y()

            if x <= world_pos.x() <= x + w and y <= world_pos.y() <= y + h:
                return obj
        
        return None
    
    def deselected_objects(self, object: BaseObject) -> None:
        for obj in self.objects:
            if obj == object:
                continue

            obj.selected = False
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

    # KeyBoard Events
    #region
    def keyPressEvent(self, event: QKeyEvent) -> None:
        super().keyPressEvent(event)

        key = event.key()

        # Object Deselection
        if key == Qt.Key.Key_Escape and self.selected_object:
            self.selected_object.selected = False
            self.selected_object = None
            self.update()
        
        # Saving
        if event.key() == Qt.Key.Key_S and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            self._save_scene()

        # Allow Snap
        if key == Qt.Key.Key_Shift:
            self.allow_snap = True
        
    def keyReleaseEvent(self, event: QKeyEvent) -> None:
        super().keyPressEvent(event)
    
        key = event.key()

        # Snap
        if key == Qt.Key.Key_Shift:
            self.allow_snap = False
    #endregion

    # Mouse Events
    #region
    def wheelEvent(self, event: QMouseEvent) -> None:
        delta = event.angleDelta()
        
        # Multiplier so you don't have to scroll forever
        pan_speed_multiplier = 2.0 
        
        self.pan += QPointF(
            delta.x() * pan_speed_multiplier, 
            delta.y() * pan_speed_multiplier
        )

        self.update()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        super().mousePressEvent(event)

        obj = self.get_object_at(
            world_pos = self.screen_to_world(event.position())
        )

        if obj and event.buttons() == Qt.MouseButton.LeftButton:
            obj.selected = True
            self.selected_object = obj
            self.deselected_objects(obj)

            self.drag_offset = self.screen_to_world(event.position()) - obj.position
        
        self.update()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        super().mouseMoveEvent(event)

        # Dragging Objects
        if self.selected_object and event.buttons() == Qt.MouseButton.LeftButton:
            world_coords = self.screen_to_world(event.position())
            
            raw_x = world_coords.x() - self.drag_offset.x()
            raw_y = world_coords.y() - self.drag_offset.y()
        
            if self.allow_snap:
                self.selected_object.move_to(
                    round(raw_x / self.snap) * self.snap,
                    round(raw_y / self.snap) * self.snap
                )
            
            else:
                self.selected_object.move_to(
                    raw_x, raw_y
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

        painter.setPen(QPen(QColor(self.theme["x_axis"])))

        world_x = start_world_x
        while world_x <= end_world_x:
            screen_x = (world_x + self.pan.x()) * self.zoom
            painter.drawLine(int(screen_x), 0, int(screen_x), self.height())
            world_x += self.snap
        
        painter.setPen(QPen(QColor(self.theme["y_axis"])))

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
        painter.setPen(QPen(QColor(self.theme["coord_text"])))

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
                    painter.drawText(int(screen_x) + 3, 18, str(int(world_x)))
            world_x += self.snap
        
        # Draw Y-axis coordinate text numbers
        world_y = start_world_y
        while world_y <= end_world_y:
            if int(world_y) != 0:
                screen_y = (world_y + self.pan.y()) * self.zoom
                if screen_y > 20:
                    painter.drawText(10, int(screen_y) - 3, str(int(world_y)))
            world_y += self.snap
        
    def draw_origin(self, painter: QPainter) -> None:
        origin_screen = self.world_to_screen(QPointF(0, 0))
        x, y = int(origin_screen.x()), int(origin_screen.y())

        size = 8
        painter.setPen(QPen(QColor(self.theme["origin"]), 2))
        painter.drawLine(x - size, y, x + size, y)
        painter.drawLine(x, y - size, x, y + size)

        # "0,0" label
        painter.setFont(QFont("Arial", 8))
        painter.setPen(QPen(QColor(self.theme["origin"])))
        painter.drawText(x + 6, y - 4, "0, 0")

    def draw_object(self, painter: QPainter, obj: BaseObject) -> None:
        screen_pos = self.world_to_screen(obj.position)

        screen_w = obj.size.x() * obj.scale.x() * self.zoom
        screen_h = obj.size.y() * obj.scale.y() * self.zoom

        if obj.selected:
            painter.setPen(QPen(QColor(self.theme["selection"]), 4))
        
        else:
            painter.setPen(Qt.NoPen)
        
        painter.setBrush(QBrush(QColor(obj.color)))

        painter.drawRect(
            int(screen_pos.x()),
            int(screen_pos.y()),
            int(screen_w),
            int(screen_h)
        )

    def paintEvent(self, event) -> None:
        with QPainter(self) as painter:
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)

            margin = 7
            clip_rect = self.rect().adjusted(margin - 1, margin - 1, -margin, -margin)
            painter.setClipRect(clip_rect)

            # Background
            painter.fillRect(self.rect(), self.theme["background"])

            for obj in self.objects:
                self.draw_object(
                    painter = painter,
                    obj = obj
                )

            # Grid
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
