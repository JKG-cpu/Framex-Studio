# ========================
# QTreeWidget: Folder Tree
# ========================
from PySide6.QtWidgets import (
    QTreeWidget, QTreeWidgetItem, 
    QSplitter, QHBoxLayout, QVBoxLayout, QGridLayout, QScrollArea,
    QWidget, QLabel, QFrame,
    QApplication, QStyle,
    QStyledItemDelegate
)
from PySide6.QtGui import QColor, QKeyEvent, QMouseEvent, QPalette, QShortcut
from PySide6.QtCore import Qt, Signal
from pathlib import Path
from PIL import Image as PILImage

from .base_panel import Panel
from .file_props import *

__all__ = ["FileSystemPanel"]

class FileTile(QWidget):
    def __init__(self, entry: Path) -> None:
        super().__init__(None)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(f"{entry.stem}"))

class FilePreviewWidget(QWidget):
    def __init__(self, parent = None) -> None:
        super().__init__(parent)

        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setObjectName("FilePreviewWidget")

        self._scroll = QScrollArea()
        self._scroll.setWidgetResizable(True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._scroll)

    def update_grid(self, path: Path) -> None:
        old_widgets = self._scroll.takeWidget()
        if old_widgets:
            old_widgets.deleteLater()

        container = QWidget()
        grid = QGridLayout(container)
        grid.setSpacing(8)
        grid.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        if path.is_dir():
            entries = sorted(path.iterdir(), key = lambda p: (p.is_file(), p.name))
            for i, entry in enumerate(entries):
                tile = FileTile(entry)
                row, col = divmod(i, 5)
                grid.addWidget(tile)
            
            self._scroll.setWidget(container)

        else:
            grid.addWidget(FileTile(path))
            self._scroll.setWidget(container)

class FileSystemWidget(QTreeWidget):
    item_selected = Signal(Path)

    def __init__(self, theme: dict[str, str], file_path: str, parent = None) -> None:
        super().__init__(parent)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)

        self.theme = theme
        self.file_path: Path = Path(file_path)

        self.setObjectName("FileSystemWidget")

        self.setColumnCount(1)
        self.setHeaderLabel("Explorer")
        self.header().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setIndentation(25)
        self.setAnimated(True)

        self._build_tree(self, self._load_entries())

        self.currentItemChanged.connect(self._on_item_changed)

    def _load_entries(self, path: Path = None) -> list:
        path = path or self.file_path
        folders = []
        files = []

        for entry in sorted(path.iterdir()):
            if entry.is_dir():
                folders.append((entry.stem, self._load_entries(entry), "Folder", entry))
            else:
                files.append((entry.stem, str(entry.suffix) if entry.suffix else "None", entry))

        return folders + files

    def _build_tree(self, parent, entries: list[tuple[str, str, str] | tuple[str, str]]) -> None:
        for entry in entries:
            if len(entry) == 4:
                name, content, _, path = entry
            elif len(entry) == 3:
                name, content, path = entry

            if isinstance(content, list):
                item = QTreeWidgetItem(parent, [name])
                item.setChildIndicatorPolicy(QTreeWidgetItem.ChildIndicatorPolicy.ShowIndicator)
                item.setForeground(0, QColor(self.theme["folder"]))
                if content: item.setExpanded(True)
                item.setData(0, Qt.UserRole, path)
                self._build_tree(item, content)

            else:
                item = QTreeWidgetItem(parent, [name])
                item.setData(0, Qt.UserRole, path)
                item.setForeground(0, QColor(self.theme["file"]))

    def _on_item_changed(self, current, previous) -> None:
        if current is None:
            return

        path = current.data(0, Qt.UserRole)

        if path:
            self.item_selected.emit(path)

    # Key Presses
    def keyPressEvent(self, event: QKeyEvent) -> None:
        key = event.key()

        if key == Qt.Key.Key_Escape:
            self.clearSelection()
        
        super().keyPressEvent(event)

class FileSystemPanel(Panel):
    def __init__(self, theme: dict[str, str], file_path: str, parent = None) -> None:
        super().__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)

        self.theme = theme
        self.setObjectName("FileSystemPanel")

        self.file_system_widget = FileSystemWidget(
            theme = self.theme,
            file_path = file_path
        )
        self.file_system_widget.item_selected.connect(self._on_item_selected)

        self.file_preview = FilePreviewWidget()

        splitter = QSplitter(orientation = Qt.Horizontal)
        splitter.setHandleWidth(0)
        splitter.addWidget(self.file_system_widget)
        splitter.addWidget(self.file_preview)

        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 5)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(splitter)

    def _on_item_selected(self, path: Path) -> None:
        self.file_preview.update_grid(path)
