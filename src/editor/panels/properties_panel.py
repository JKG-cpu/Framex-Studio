# ===============================
# QWidget: Object Properties Form
# ===============================
from PySide6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QCheckBox,
    QSpinBox,
    QDoubleSpinBox,
    QPushButton,
    QColorDialog,
    QWidget,
)
from PySide6.QtCore import Qt, Signal

from .base_panel import Panel
from ...runtime import BaseObject

__all__ = ["PropertiesPanel"]


class PropertiesPanel(Panel):
    object_updated = Signal(BaseObject)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("PropertiesPanel")

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.obj: BaseObject | None = None

    # Layout Helpers
    # region
    def _clear_layout(self, layout) -> None:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()
            else:
                sub_layout = item.layout()
                if sub_layout is not None:
                    self._clear_layout(sub_layout)

    def _add_row(self, label: str, widget: QWidget) -> None:
        row = QWidget()
        row_layout = QHBoxLayout(row)
        row_layout.setContentsMargins(0, 0, 0, 0)

        row_layout.addWidget(QLabel(label))
        row_layout.addWidget(widget)

        self.layout.addWidget(row)

    def _emit_update(self) -> None:
        self.object_updated.emit(self.obj)

    # endregion

    # Build Form
    # region
    def update_object(self, obj: BaseObject) -> None:
        self.obj = obj
        self._clear_layout(self.layout)

        self.layout.addWidget(QLabel(obj.name))

        # Name
        name_edit = QLineEdit(obj.name)
        name_edit.editingFinished.connect(lambda: self._set_name(name_edit.text()))
        self._add_row("Name", name_edit)

        # Active
        active_check = QCheckBox()
        active_check.setChecked(obj.active)
        active_check.toggled.connect(self._set_active)
        self._add_row("Active", active_check)

        # Layer
        layer_spin = QSpinBox()
        layer_spin.setRange(-1000, 1000)
        layer_spin.setValue(obj.layer)
        layer_spin.valueChanged.connect(self._set_layer)
        self._add_row("Layer", layer_spin)

        # Color
        color_button = QPushButton(obj.color)
        color_button.setStyleSheet(f"background-color: {obj.color};")
        color_button.clicked.connect(lambda: self._pick_color(color_button))
        self._add_row("Color", color_button)

        # Position
        pos_x = self._make_double_spin(obj.position.x())
        pos_y = self._make_double_spin(obj.position.y())
        pos_x.valueChanged.connect(
            lambda _: self._set_position(pos_x.value(), pos_y.value())
        )
        pos_y.valueChanged.connect(
            lambda _: self._set_position(pos_x.value(), pos_y.value())
        )
        self._add_row("Position X", pos_x)
        self._add_row("Position Y", pos_y)

        # Rotation
        rotation_spin = self._make_double_spin(obj.rotation, minimum=-360, maximum=360)
        rotation_spin.valueChanged.connect(self._set_rotation)
        self._add_row("Rotation", rotation_spin)

        # Scale
        scale_x = self._make_double_spin(obj.scale.x())
        scale_y = self._make_double_spin(obj.scale.y())
        scale_x.valueChanged.connect(
            lambda _: self._set_scale(scale_x.value(), scale_y.value())
        )
        scale_y.valueChanged.connect(
            lambda _: self._set_scale(scale_x.value(), scale_y.value())
        )
        self._add_row("Scale X", scale_x)
        self._add_row("Scale Y", scale_y)

        # Size
        size_w = self._make_double_spin(obj.size.x())
        size_h = self._make_double_spin(obj.size.y())
        size_w.valueChanged.connect(
            lambda _: self._set_size(size_w.value(), size_h.value())
        )
        size_h.valueChanged.connect(
            lambda _: self._set_size(size_w.value(), size_h.value())
        )
        self._add_row("Size W", size_w)
        self._add_row("Size H", size_h)

        # Tags
        tags_edit = QLineEdit(", ".join(obj.tag))
        tags_edit.editingFinished.connect(lambda: self._set_tags(tags_edit.text()))
        self._add_row("Tags", tags_edit)

    def _make_double_spin(
        self, value: float, minimum: float = -99999, maximum: float = 99999
    ) -> QDoubleSpinBox:
        spin = QDoubleSpinBox()
        spin.setRange(minimum, maximum)
        spin.setValue(value)
        spin.setDecimals(2)
        return spin

    # endregion

    # Setters (write back to obj, then notify)
    # region
    def _set_name(self, value: str) -> None:
        self.obj.name = value
        self._emit_update()

    def _set_active(self, value: bool) -> None:
        if value != self.obj.active:
            self.obj.toggle_active()
            self._emit_update()

    def _set_layer(self, value: int) -> None:
        self.obj.layer = value
        self._emit_update()

    def _pick_color(self, button: QPushButton) -> None:
        color = QColorDialog.getColor()
        if color.isValid():
            hex_color = color.name()
            self.obj.color = hex_color
            button.setText(hex_color)
            button.setStyleSheet(f"background-color: {hex_color};")
            self._emit_update()

    def _set_position(self, x: float, y: float) -> None:
        self.obj.move_to(x, y)
        self._emit_update()

    def _set_rotation(self, value: float) -> None:
        self.obj.rotate(value)
        self._emit_update()

    def _set_scale(self, w: float, h: float) -> None:
        self.obj.scale_to(w, h)
        self._emit_update()

    def _set_size(self, w: float, h: float) -> None:
        self.obj.resize(w, h)
        self._emit_update()

    def _set_tags(self, text: str) -> None:
        tags = [t.strip() for t in text.split(",") if t.strip()]
        self.obj.tag = tags
        self._emit_update()

    # endregion
