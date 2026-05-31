# ========================
# QTreeWidget: Folder Tree
# ========================
from PySide6.QtWidgets import (
    QVBoxLayout, QLabel
)

from .base_panel import Panel

__all__ = ["FileSystemPanel"]

class FileSystemPanel(Panel):
    def __init__(self, parent = None) -> None:
        super().__init__(parent)
        self.setObjectName("FileSystemPanel")
        
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("File System Panel"))
        layout.addStretch()

