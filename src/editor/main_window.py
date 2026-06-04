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
import qdarktheme

from .panels import *
from .scene_editor import SceneEditor

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
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Framex Studio Editor")
        self.resize(1600, 1000)

        # Color Schemes
        self.mode: Literal["dark", "light"] = "dark"

        self.scene_view_colors = {
            "dark": {
                "background": "#1E1E1E",
                "coord_text": "#4A90B8",
                "x_axis": "#D16969",
                "y_axis": "#4A90B8",
                "origin": "#FF5555",
                "selection": "#6CB6FF",
                "text": "#D4D4D4"
            },
            "light": {
                "background": "#F7F7F7",
                "coord_text": "#2E75A0",
                "x_axis": "#CC5555",
                "y_axis": "#2E75A0",
                "origin": "#E53935",
                "selection": "#1976D2",
                "text": "#222222"
            }
        }

        # Scene Editor
        self.scene_editor = SceneEditor()

        # Top Row
        self.scene_view = SceneView(
            item_colors = self.scene_view_colors.get(self.mode)
        )
        self.properties_panel = PropertiesPanel()

        top_splitter = QSplitter(orientation = Qt.Horizontal)
        top_splitter.setHandleWidth(0)
        
        top_splitter.addWidget(self.scene_view)
        top_splitter.addWidget(self.properties_panel)

        # Bottom
        self.file_system_panel = FileSystemPanel()

        main_splitter = QSplitter(Qt.Vertical)
        main_splitter.setHandleWidth(0)

        main_splitter.addWidget(top_splitter)
        main_splitter.addWidget(self.file_system_panel)
        main_splitter.setStretchFactor(0, 3)
        main_splitter.setStretchFactor(1, 1)

        self.setCentralWidget(main_splitter)
