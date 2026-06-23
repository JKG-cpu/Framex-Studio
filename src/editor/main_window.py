# =============================
# Main PySide6 Window (Layout)
# =============================
from PySide6.QtWidgets import (
    QMainWindow,
    QSplitter, QHBoxLayout,
    QWidget
)
from PySide6.QtCore import Qt
from os.path import join

from .panels import *
from .scene_editor import SceneEditor
from ..settings import ThemeManager

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
        self.setObjectName("MainWindow")
        self.resize(1600, 1000)
        self.setContentsMargins(12, 12, 12, 12)

        # Theme Manager
        self.theme_manager = ThemeManager()
        self.theme_manager.apply()

        # Options Bar
        self.options_widget = QWidget()
        self.options_widget.setObjectName("SettingsBar")
        self.options_widget.setMaximumHeight(30)

        # Scene Editor
        self.scene_editor = SceneEditor()

        # Top Row
        self.hierarchy_panel = HierarchyPanel()
        self.scene_view = SceneView(
            theme = self.theme_manager.scene_view_colors
        )
        self.properties_panel = PropertiesPanel()

        top_splitter = QSplitter(orientation = Qt.Horizontal)
        top_splitter.setHandleWidth(0)
        
        top_splitter.addWidget(self.hierarchy_panel)
        top_splitter.addWidget(self.scene_view)
        top_splitter.addWidget(self.properties_panel)

        # Bottom
        self.file_system_panel = FileSystemPanel(
            theme = self.theme_manager.file_system_colors,
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
