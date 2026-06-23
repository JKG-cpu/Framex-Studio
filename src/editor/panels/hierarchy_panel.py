# ===============================
# QWidget: Heirarchy Panel
# ===============================
from PySide6.QtWidgets import QVBoxLayout, QLabel

from .base_panel import Panel

__all__ = ["HierarchyPanel"]

class HierarchyPanel(Panel):
    def __init__(self, parent = None) -> None:
        super().__init__(parent)

        self.setObjectName("HeirarchyPanel")

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Heirarchy Panel"))
        layout.addStretch()