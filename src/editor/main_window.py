# =============================
# Main PySide6 Window (Layout)
# =============================
from PySide6.QtWidgets import (
    QMainWindow,
    QSplitter, QHBoxLayout,
    QWidget
)
from PySide6.QtCore import Qt, QThread, Signal, QObject
from os.path import join

from .panels import *
from .scene_editor import SceneEditor
from ..settings import ThemeManager
from ..runtime import BaseObject

__all__ = ["MainWindow"]

class SceneLoader(QObject):
    finished = Signal(dict)

    def __init__(self, scene_editor, path):
        super().__init__()
        self.scene_editor = scene_editor
        self.path = path

    def run(self):
        self.scene_editor.select_scene(self.path)
        self.finished.emit(self.scene_editor.scene_data)

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
        self.scene_view.save_scene.connect(self._save_scene)
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
        self.file_system_panel.scene_selected.connect(self._scene_selected) 

        main_splitter = QSplitter(Qt.Vertical)
        main_splitter.setHandleWidth(0)

        main_splitter.addWidget(self.options_widget)
        main_splitter.addWidget(top_splitter)
        main_splitter.addWidget(self.file_system_panel)
        
        main_splitter.setStretchFactor(0, 1)
        main_splitter.setStretchFactor(1, 7)
        main_splitter.setStretchFactor(2, 1)

        self.setCentralWidget(main_splitter)

        self._scene_cache: dict[str, dict] = {}

    def _scene_selected(self, path) -> None:
        if path in self._scene_cache:
            self.scene_view.select_scene(self._scene_cache[path])
            return

        self._thread = QThread()
        self._loader = SceneLoader(self.scene_editor, path)
        self._loader.moveToThread(self._thread)

        self._thread.started.connect(self._loader.run)
        self._loader.finished.connect(self._on_scene_loaded)
        self._loader.finished.connect(self._thread.quit)

        self._thread.start()

    def _on_scene_loaded(self, scene_data: dict) -> None:
        self.scene_view.select_scene(scene_data)
        self.lu_path = self._loader.path
        self._scene_cache[self._loader.path] = scene_data

    def _save_scene(self, scene_data: dict) -> None:
        self.scene_editor.save_scene(self.lu_path, scene_data)
