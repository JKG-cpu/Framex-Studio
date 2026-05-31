# =============================
# Main PySide6 Window (Layout)
# =============================
from PySide6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QWidget
)
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

        # Central Widget
        central = QWidget()
        self.setCentralWidget(central)
        root_layout = QVBoxLayout(central)

        # Scene Editor
        self.scene_editor = SceneEditor()

        # Scene View + Properties
        top = QHBoxLayout()
        self.scene_view = SceneView(scene_editor = self.scene_editor)
        self.properties_panel = PropertiesPanel()
        top.addWidget(self.scene_view)
        top.addWidget(self.properties_panel)

        self.file_system_panel = FileSystemPanel()

        root_layout.addLayout(top)
        root_layout.addWidget(self.file_system_panel)