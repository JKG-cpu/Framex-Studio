import json
from pathlib import Path
from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QApplication

class ThemeManager(QObject):
    theme_changed = Signal(str)

    def __init__(self) -> None:
        super().__init__()
        self._file_path = Path(__file__).parent / "color.json"
        self._mode = "dark"
        self._data = {}
        self._base = ""
        self._load()

    def _load(self) -> None:
        with open(self._file_path) as f:
            self._data = json.load(f)
        self._mode = self._data.get("mode", "dark")

    def _get_colors(self, section: str) -> dict:
        return self._data.get(section, {}).get(self._mode, {})

    @property
    def main_colors(self) -> dict:
        return self._get_colors("main_colors")

    @property
    def scene_view_colors(self) -> dict:
        return self._get_colors("scene_view")

    @property
    def file_system_colors(self) -> dict:
        return self._get_colors("file_system")

    def generate_stylesheet(self) -> str:
        main = self.main_colors
        fs = self.file_system_colors

        return f"""
            QMainWindow#MainWindow {{
                background-color: {main["background"]};
                color: {main["text"]};
            }}

            SceneView, PropertiesPanel, FileSystemPanel {{
                border: 2px solid {main["border"]};
            }}

            QFrame#SceneviewTopBar, QFrame#SceneviewEditBar, QFrame#SceneviewBottomBar {{
                background: {main["background_alt"]};
            }}

            PropertiesPanel {{
                background-color: {main["background"]};
            }}

            FileSystemPanel {{
                background-color: {fs["background"]};
            }}

            FileSystemWidget#FileSystemWidget {{
                background-color: {fs["background_alt"]};
                border: 2px solid {fs["border"]};
                outline: none;
            }}

            FileSystemWidget::item {{
                padding: 4px 0px;
                background-color: {fs["background_alt"]};
            }}

            FileSystemWidget::item:hover {{
                background-color: {fs["hover"]};
            }}

            FileSystemWidget::item:selected {{
                background-color: {fs["selection"]};
                color: {fs["selection_text"]};
            }}

            QHeaderView::section {{
                background-color: {fs["header_background"]};
                color: {fs["text"]};
                padding: 4px;
                border: none;
                border-bottom: 2px solid {fs["border"]};
            }}

            #FilePreviewWidget {{
                border: 2px solid {main["border"]};
            }}

            #FilePropertiesWidget * {{
                border: 1px solid {main["border"]};
                padding: 10px;
                margin-top: 5px;
                margin-bottom: 5px;
            }}

            #FilePropertiesWidget QLabel {{
                qproperty-alignment: AlignCenter;
            }}

            QPushButton {{
                background: transparent;
                border: none;
            }}
        """

    def apply(self) -> None:
        app = QApplication.instance()
        if app is None:
            return

        if not self._base:
            self._base = app.styleSheet() or ""

        app.setStyleSheet(self._base + self.generate_stylesheet())
        self.theme_changed.emit(self._mode)

    @property
    def mode(self) -> str:
        return self._mode

    def set_mode(self, mode: str) -> None:
        self._mode = mode
        self._data["mode"] = mode
        self.apply()

    def toggle_theme(self) -> None:
        new_mode = "light" if self._mode == "dark" else "dark"
        self.set_mode(new_mode)
