# ========================
# QTreeWidget: Folder Tree
# ========================
from PySide6.QtWidgets import (
    QTreeWidget, QTreeWidgetItem, 
    QSplitter, QHBoxLayout, QVBoxLayout,
    QWidget, QLabel, QFrame,
    QApplication, QStyle,
    QStyledItemDelegate
)
from PySide6.QtGui import QColor, QKeyEvent, QMouseEvent, QPalette
from PySide6.QtCore import Qt, Signal
from pathlib import Path
from PIL import Image as PILImage

from .base_panel import Panel
from .file_props import *

__all__ = ["FileSystemPanel"]

class PreserveForegroundDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        foreground = index.data(Qt.ItemDataRole.ForegroundRole)
        if foreground:
            option.palette.setColor(
                QPalette.ColorRole.HighlightedText,
                foreground.color()
            )

class FilePreviewWidget(QWidget):
    def __init__(self, parent = None) -> None:
        super().__init__(parent)

        self.setObjectName("FilePreviewWidget")
        self.setStyleSheet("""
            FilePreviewWidget { border: 2px solid grey; }
        """)

class FilePropertiesWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.setObjectName("FilePropertiesWidget")
        self.setStyleSheet("""
            #FilePropertiesWidget * { 
                border: 1px solid grey; 
                padding: 10px;
                margin-top: 5px;
                margin-bottom: 5px;
            }
            #FilePropertiesWidget QLabel { 
                qproperty-alignment: AlignCenter;
            }
        """
        )

        self.WIDGET_REGISTRY = {
            File: self._build_file,
            Folder: self._build_folder,
            Image: self._build_image
        }

        layout = QVBoxLayout(self)

        self.name = QLabel("No file or folder selected")

        layout.addWidget(self.name)
        layout.addStretch()
    
    def _build_file(self, props: File) -> list: 
        """Returns QLabel of File Properties"""
        return [
            QLabel(f"Size: {props.size}")
        ]

    def _build_folder(self, props: Folder) -> list: 
        """Returns QLabels of Folder Properties"""
        return [
            QLabel(f"Size: {props.total_size}"),
            QLabel(f"Content Amount: {props.item_count}")
        ]

    def _build_image(self, props: Image) -> list:
        """Returns QLabels of Image Properties"""
        return [
            QLabel(f"Size: {props.size}"),
            QLabel(f"Image Size: {props.width}x{props.height}"),
            QLabel(f"Image Type: {props.format}")
        ]

    def update_properties(self, props: File | Folder) -> None:
        while self.layout().count() > 1:
            item = self.layout().takeAt(1)
            if item.widget():
                item.widget().deleteLater()
        
        self.name.setText(props.name)

        builder = self.WIDGET_REGISTRY.get(type(props))
        if builder:
            for widget in builder(props):
                self.layout().addWidget(widget)
        
        self.layout().addStretch()

class FileSystemWidget(QTreeWidget):
    item_selected = Signal(object)

    def __init__(self, theme: dict[str, str], file_path: str, parent = None) -> None:
        super().__init__(parent)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setItemDelegate(PreserveForegroundDelegate(self))

        self.theme = theme
        self.file_path: Path = Path(file_path)

        self.setObjectName("FileSystemWidget")
        self.setStyleSheet(f"""
            FileSystemWidget {{
                background-color: {self.theme.get("background_alt")};
                border: 2px solid {self.theme.get("border")};
                outline: none;
            }}

            FileSystemWidget::item {{ 
                padding: 4px 0px;
                background-color: {self.theme.get("background_alt")};
            }}

            FileSystemWidget::item:hover {{
                background-color: {self.theme.get("hover")};
            }}

            FileSystemWidget::item:selected {{
                background-color: {self.theme.get("background_alt")};
            }}

            QHeaderView::section {{
                background-color: {self.theme.get("header_background")};
                color: {self.theme.get("text")};
                padding: 4px;
                border: none;
                border-bottom: 2px solid {self.theme.get("border")};
            }}
        """)

        self.setColumnCount(1)
        self.setHeaderLabel("Explorer")
        self.header().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.setIndentation(25)
        self.setAnimated(True)
        
        self.itemClicked.connect(self._on_file_selected)

        self._build_tree(self, self._load_entries())

    def _load_entries(self, path: Path = None) -> list:
        path = path or self.file_path
        folders = []
        files = []

        for entry in sorted(path.iterdir()):
            if entry.is_dir():
                folders.append((entry.name, self._load_entries(entry), "Folder", entry))
            else:
                files.append((entry.name, str(entry.suffix) if entry.suffix else "None", entry))

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

    # Formatting / Theme
    def _format_size(self, size: int) -> str:
        for unit in ("B", "KB", "MB", "GB"):
            if size < 1024:
                return f"{size} {unit}"
            size /= 1024

    # File Selected => File Properties Widget
    def _on_file_selected(self, item: QTreeWidgetItem, column: int) -> None:
        path: Path = item.data(0, Qt.UserRole)
        if path is None:
            return

        if path.is_dir():
            contents = list(path.iterdir())
            props = Folder(
                name = path.name,
                total_size = self._format_size(sum(f.stat().st_size for f in contents if f.is_file())),
                item_count = len(contents)
            )

        elif path.suffix.lower() in (".png", ".jpg", ".jpeg", ".bmp", ".gif"):
            stat = path.stat()

            try:
                with PILImage.open(path) as img:
                    w, h = img.size

                props = Image(
                    name = path.name,
                    size = self._format_size(path.stat().st_size),
                    width = w,
                    height = h,
                    format = path.suffix.upper().lstrip(".")
                )

            except:
                props = Image(
                    name = path.name,
                    size = self._format_size(path.stat().st_size),
                    format = path.suffix.upper().lstrip(".")
                )
        
        else:
            props = File(
                name = path.name,
                size = self._format_size(path.stat().st_size)
            )

        self.item_selected.emit(props)

class FileSystemPanel(Panel):
    def __init__(self, theme: dict[str, str], file_path: str, parent = None) -> None:
        super().__init__(parent)

        self.theme = theme
        self.setObjectName("FileSystemPanel")
        self.setStyleSheet(f"""
            FileSystemPanel {{
                background-color: {self.theme.get("background")}
            }}
        """)

        self.file_system_widget = FileSystemWidget(
            theme = self.theme,
            file_path = file_path
        )
        self.file_system_widget.item_selected.connect(self._on_file_selected)

        self.file_preview = FilePreviewWidget()

        self.file_properties = FilePropertiesWidget()

        splitter = QSplitter(orientation = Qt.Horizontal)
        splitter.setHandleWidth(0)
        splitter.addWidget(self.file_system_widget)
        splitter.addWidget(self.file_preview)
        splitter.addWidget(self.file_properties)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(splitter)
    
    def _on_file_selected(self, props: File | Folder) -> None:
        self.file_properties.update_properties(props)
