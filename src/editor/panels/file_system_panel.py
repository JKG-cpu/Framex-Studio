# ========================
# QTreeWidget: Folder Tree
# ========================
from PySide6.QtWidgets import (
    QTreeWidget, QTreeWidgetItem, 
    QSplitter, QHBoxLayout, QVBoxLayout,
    QWidget, QLabel, QFrame
)
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt, Signal
from pathlib import Path

from .base_panel import Panel

__all__ = ["FileSystemPanel"]

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

        layout = QVBoxLayout(self)
        
        self.name = QLabel("No file or folder selected")

        layout.addWidget(self.name)

        container = QFrame()
        hbox = QHBoxLayout(container)
        
        self.type = QLabel("No file selected")
        hbox.addWidget(QLabel("File Type: "))
        hbox.addWidget(self.type)
        
        layout.addWidget(container)

        container = QFrame()
        hbox = QHBoxLayout(container)
        hbox.addWidget(QLabel("Remove"))
        hbox.addWidget(QLabel("Duplicate"))

        layout.addWidget(container)

        layout.addStretch()

class FilePreviewWidget(QWidget):
    def __init__(self, parent = None) -> None:
        super().__init__(parent)

        self.setObjectName("FilePreviewWidget")
        self.setStyleSheet("""
            FilePreviewWidget { border: 2px solid grey; }
        """)

class FileSystemWidget(QTreeWidget):
    item_selected = Signal(str, bool)

    def __init__(self, item_colors: dict[str, str], file_path: str, parent = None) -> None:
        super().__init__(parent)
        self.item_colors = item_colors
        self.file_path: Path = Path(file_path)

        self.setObjectName("FileSystemWidget")
        self.setStyleSheet("""
            FileSystemWidget::item { padding: 4px 0px; } 
            FileSystemWidget { border: 2px solid grey; }
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
        entries = []

        for entry in sorted(path.iterdir()):
            if entry.is_dir():
                entries.append((entry.stem, self._load_entries(entry), "Folder"))
            else:
                entries.append((entry.stem, str(entry.suffix) if entry.suffix else "None"))

        return entries

    def _build_tree(self, parent, entries: list[tuple[str, str, str] | tuple[str, str]]) -> None:
        for entry in entries:
            if len(entry) == 3:
                name, content, fname = entry
            else:
                name, content = entry

            if isinstance(content, list):
                item = QTreeWidgetItem(parent, [name])
                item.setForeground(0, QColor(self.item_colors["folder"]))
                item.setExpanded(True)
                self._build_tree(item, content)

            else:
                item = QTreeWidgetItem(parent, [name])
                item.setForeground(0, QColor(self._get_file_color(content)))
                item.setForeground(1, QColor(self.item_colors["file_size"]))

    def _get_file_color(self, extension: str) -> str:
        ext_map = {
            ".scene": "scene_file",
            ".py":    "script_file",
            ".cfg":   "config_file",
            ".ini":   "config_file",
            ".toml":  "config_file",
            ".json":  "config_file",
            ".md":    "doc_file",
            ".txt":   "doc_file",
            ".rst":   "doc_file",
        }
        key = ext_map.get(extension, "file")
        return self.item_colors[key]

    def _on_file_selected(self, item: QTreeWidgetItem, column: int) -> None:
        is_folder = item.childCount() > 0
        self.item_selected.emit(item.text(0), is_folder)

class FileSystemPanel(Panel):
    def __init__(self, item_colors: dict[str, str], file_path: str, parent = None) -> None:
        super().__init__(parent)

        self.item_colors = item_colors
        self.setObjectName("FileSystemPanel")

        self.file_system_widget = FileSystemWidget(
            item_colors = self.item_colors,
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
    
    def _on_file_selected(self, name: str, is_folder: bool) -> None:
        self.file_properties.name.setText(name)
