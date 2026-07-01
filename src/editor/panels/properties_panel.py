# ===============================
# QWidget: Object Properties Form
# ===============================
from PySide6.QtWidgets import QVBoxLayout, QLabel

from .base_panel import Panel

__all__ = ["PropertiesPanel"]


class PropertiesPanel(Panel):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("PropertiesPanel")

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Properties Panel"))
        layout.addStretch()
