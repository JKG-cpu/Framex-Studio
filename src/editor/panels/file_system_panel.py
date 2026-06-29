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
from PySide6.QtGui import (
    QColor, QPalette, QPixmap, QImage,
    QKeyEvent, QMouseEvent, QShortcut
)
from PySide6.QtCore import Qt, Signal
from PIL import Image as PILImage
from pathlib import Path
from os.path import join

from .base_panel import Panel
from .file_props import *

__all__ = ["FileSystemPanel"]

HEAD_PATH = Path(__file__).parent.parent.parent / "resources" / "icons" / "Files"
ICON_PATHS = {
    "file": Path(join(HEAD_PATH, "File.png")),
    "json": Path(join(HEAD_PATH, "Json File.png")),
    "py": Path(join(HEAD_PATH, "Python File.png")),
    "python": Path(join(HEAD_PATH, "Python File.png")),
    "tmx": Path(join(HEAD_PATH, "TMX File.png"))
}

class FileTile(QWidget):
    def __init__(self, entry: Path) -> None:
        super().__init__(None)

        label = QLabel()

        pixmap = QPixmap(str(self._get_icon(entry.suffix)))
        pixmap = self._trim_transparent(pixmap)
        label.setPixmap(
            pixmap.scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.FastTransformation)
        )

        filename = QLabel(self._get_file_name(entry.name))

        layout = QVBoxLayout(self)

        layout.addWidget(label)
        layout.addWidget(filename)

    def _trim_transparent(self, pixmap: QPixmap) -> QPixmap:
        import numpy as np

        image = pixmap.toImage().convertToFormat(QImage.Format.Format_ARGB32)
        ptr = image.bits()
        arr = np.frombuffer(ptr, dtype=np.uint8).reshape((image.height(), image.width(), 4))

        alpha = arr[:, :, 3]
        rows = np.any(alpha > 0, axis=1)
        cols = np.any(alpha > 0, axis=0)

        if not rows.any():
            return pixmap

        min_y, max_y = np.where(rows)[0][[0, -1]]
        min_x, max_x = np.where(cols)[0][[0, -1]]

        cropped = image.copy(int(min_x), int(min_y), int(max_x - min_x + 1), int(max_y - min_y + 1))
        return QPixmap.fromImage(cropped)

    def _get_icon(self, extension: str) -> str:
        path = ICON_PATHS.get(extension.lstrip("."), ICON_PATHS["file"])
        return str(path)

    def _get_file_name(self, full_name: str) -> None:
        return full_name.split(".")[0]

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
        grid.setAlignment(Qt.AlignmentFlag.AlignTop)

        if path.is_dir():
            entries = sorted(path.iterdir(), key = lambda p: (p.is_file(), p.name))
            for i, entry in enumerate(entries):
                tile = FileTile(entry)
                row, col = divmod(i, 5)
                grid.addWidget(tile, row, col)
            
            self._scroll.setWidget(container)

        else:
            grid.addWidget(FileTile(path))
            self._scroll.setWidget(container)

class FileSystemWidget(QTreeWidget):
    item_selected = Signal(Path)
    scene_selected = Signal(Path)

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

        path: Path = current.data(0, Qt.UserRole)

        if path:
            if ".scene" in path.name:
                self.scene_selected.emit(path)

            self.item_selected.emit(path)

    # Key Presses
    def keyPressEvent(self, event: QKeyEvent) -> None:
        key = event.key()

        if key == Qt.Key.Key_Escape:
            self.clearSelection()
        
        super().keyPressEvent(event)

class FileSystemPanel(Panel):
    scene_selected = Signal(Path)

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
        self.file_system_widget.scene_selected.connect(self._on_scene_selected)

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

    def _on_scene_selected(self, path: Path) -> None:
        self.scene_selected.emit(path)
