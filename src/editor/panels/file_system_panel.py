# ========================
# QTreeWidget: Folder Tree
# ========================
from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem
from PySide6.QtGui import QColor
from pathlib import Path

from .base_panel import Panel

__all__ = ["FileSystemPanel"]

class FileSystemPanel(QTreeWidget):
    def __init__(self, item_colors: dict[str, str], file_path: str, parent=None) -> None:
        super().__init__(parent)
        self.item_colors = item_colors
        self.file_path: Path = Path(file_path)

        self.setObjectName("FileSystemPanel")
        self.setColumnCount(2)
        self.setHeaderLabels(["Name", "Size"])
        self.setColumnWidth(0, 320)
        self.setIndentation(18)
        self.setAnimated(True)

        self._build_tree(self, self._load_entries())

    def _load_entries(self, path: Path = None) -> list:
        path = path or self.file_path
        entries = []

        for entry in sorted(path.iterdir()):
            if entry.is_dir():
                entries.append((entry.name, self._load_entries(entry)))
            else:
                entries.append((entry.name, str(entry.stat().st_size)))

        return entries

    def _build_tree(self, parent, entries: list) -> None:
        for entry in entries:
            name, content = entry

            if isinstance(content, list):
                item = QTreeWidgetItem(parent, [name, ""])
                item.setForeground(0, QColor(self.item_colors["folder"]))
                item.setExpanded(True)
                self._build_tree(item, content)

            else:
                item = QTreeWidgetItem(parent, [name, content])
                item.setForeground(0, QColor(self.item_colors["file"]))
                item.setForeground(1, QColor(self.item_colors["file_size"]))