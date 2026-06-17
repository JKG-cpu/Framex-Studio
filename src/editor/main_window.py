# =============================
# Main PySide6 Window (Layout)
# =============================
from PySide6.QtWidgets import (
    QMainWindow,
    QSplitter,
    QWidget
)
from PySide6.QtCore import Qt
from typing import Literal
from os.path import join
import qdarktheme

from .panels import *
from .scene_editor import SceneEditor
from ..settings import *

__all__ = ["MainWindow"]

# Dark Mode Switch
#region
# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()

#         self.setWindowTitle("Framex Studio Editor")
#         self.resize(1600, 1000)

#         self.is_dark = True

#         layout = QVBoxLayout()
#         self.toggle_btn = QPushButton("Switch to Light Mode")
#         self.toggle_btn.clicked.connect(self.toggle_theme)
#         layout.addWidget(self.toggle_btn)

#         container = QWidget()
#         container.setLayout(layout)
#         self.setCentralWidget(container)

#     def toggle_theme(self) -> None:
#         if self.is_dark:
#             qdarktheme.setup_theme("light")
#             self.toggle_btn.setText("Switch to Dark Mode")
#             self.is_dark = False

#         else:
#             qdarktheme.setup_theme("dark")
#             self.toggle_btn.setText("Switch to Light Mode")
#             self.is_dark = True
#endregion

class MainWindow(QMainWindow):
    def __init__(self, *file_path: str) -> None:
        super().__init__()

        self.setWindowTitle("Framex Studio Editor")
        self.resize(1600, 1000)
        self.setContentsMargins(8, 8, 8, 8)

        # Color Schemes
        self.storage = Storage()

        # Options Bar
        self.options_widget = QWidget()
        self.options_widget.setMaximumHeight(20)

        # Scene Editor
        self.scene_editor = SceneEditor()

        # Top Row
        self.scene_view = SceneView(
            item_colors = self.storage.color.scene_view
        )
        self.properties_panel = PropertiesPanel()

        top_splitter = QSplitter(orientation = Qt.Horizontal)
        top_splitter.setHandleWidth(0)
        
        top_splitter.addWidget(self.scene_view)
        top_splitter.addWidget(self.properties_panel)

        # Bottom
        self.file_system_panel = FileSystemPanel(
            item_colors = self.storage.color.file_system,
            file_path = join(*file_path)
        )

        main_splitter = QSplitter(Qt.Vertical)
        main_splitter.setHandleWidth(0)

        main_splitter.addWidget(self.options_widget)
        main_splitter.addWidget(top_splitter)
        main_splitter.addWidget(self.file_system_panel)
        
        main_splitter.setStretchFactor(0, 1)
        main_splitter.setStretchFactor(1, 7)
        main_splitter.setStretchFactor(2, 1)

        self.setCentralWidget(main_splitter)
