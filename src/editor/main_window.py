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
        self.file_system_panel_colors = {
            "dark": {
                "background":           "#1E1E1E",
                "background_alt":       "#252526",
                "header_background":    "#2A2A2A",
                "text":                 "#D4D4D4",
                "text_muted":           "#8A8A8A",
                "folder":               "#4A90B8",
                "file":                 "#C8C8C8",
                "file_size":            "#8A8A8A",
                "selection":            "#2D5D8A",
                "selection_text":       "#FFFFFF",
                "hover":                "#2A3F52",
                "border":               "#3A3A3A",
                "scrollbar_bg":         "#252526",
                "scrollbar_handle":     "#4A4A4A",
                "scrollbar_handle_hover": "#5A5A5A",
                "scene_file":           "#D7BA7D",
                "script_file":          "#569CD6",
                "config_file":          "#B5CEA8",
                "doc_file":             "#CE9178",
            },
            "light": {
                "background":           "#F7F7F7",
                "background_alt":       "#EEEEEE",
                "header_background":    "#E5E5E5",
                "text":                 "#222222",
                "text_muted":           "#6E6E6E",
                "folder":               "#2E75A0",
                "file":                 "#444444",
                "file_size":            "#7A7A7A",
                "selection":            "#CFE8FF",
                "selection_text":       "#111111",
                "hover":                "#E6F2FA",
                "border":               "#C8C8C8",
                "scrollbar_bg":         "#E5E5E5",
                "scrollbar_handle":     "#B8B8B8",
                "scrollbar_handle_hover": "#A5A5A5",
                "scene_file":           "#B8860B",
                "script_file":          "#2E75A0",
                "config_file":          "#4E8C4A",
                "doc_file":             "#C96A2B",
            }
        }

        # Options Bar
        self.options_widget = QWidget()
        self.options_widget.setMaximumHeight(20)

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
        self.file_system_panel = FileSystemPanel(
            item_colors = self.file_system_panel_colors.get(self.mode),
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
