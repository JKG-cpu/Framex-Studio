import json
import qdarktheme
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

    # StyleSheet
    #region
    def generate_stylesheet(self) -> str:
        main = self.main_colors
        fs = self.file_system_colors

        return f"""
            /* Main Window */
            QMainWindow#MainWindow {{
                background-color: {main["background"]};
                color: {main["text"]};
            }}

            /* Each Panel "Section" */
            SceneView, PropertiesPanel, FileSystemPanel {{
                border: 2px solid {main["border"]};
            }}

            /* Different Bars in SceneView */
            QFrame#SceneviewTopBar, QFrame#SceneviewEditBar, QFrame#SceneviewBottomBar {{
                background: {main["background_alt"]};
            }}

            PropertiesPanel {{
                background-color: {main["background"]};
            }}

            FileSystemPanel {{
                background-color: {fs["background"]};
            }}

            /* File System Panel */
            FileSystemWidget#FileSystemWidget {{
                background-color: {fs["background_alt"]};
                border: 2px solid {fs["border"]};
                border-radius: 0;
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

            /* Text on top of file explorer */
            QHeaderView::section {{
                background-color: {fs["header_background"]};
                color: {fs["text"]};
                padding: 4px;
                border: none;
                border-bottom: 2px solid {fs["border"]};
            }}

            /* File Preview Widget */
            FilePreviewWidget#FilePreviewWidget {{
                background-color: {fs["background_alt"]};
                border: 2px solid {fs["border"]};
                outline: none;
            }}

            /* File Properties Widget */
            #FilePropertiesWidget {{
                background-color: {fs["background_alt"]};
                border: 2px solid {fs["border"]};
                outline: none;
            }}

            #FilePropertiesWidget * {{
                border: 2px solid {main["border"]};
                border-radius: 8px;
                padding: 10px;
                margin-top: 5px;
                margin-bottom: 5px;
            }}

            #FilePropertiesWidget QLabel {{
                qproperty-alignment: AlignCenter;
            }}

            /* Buttons */
            QPushButton {{
                background: transparent;
                border: none;
            }}

            QPushButton:hover {{
                background: transparent;
            }}
        """

    def apply(self) -> None:
        app = QApplication.instance()
        if app is None:
            return

        qdarktheme.setup_theme(self._mode)
        app.setStyleSheet(app.styleSheet() + self.generate_stylesheet())
        self.theme_changed.emit(self._mode)
    #endregion

    # Mode
    #region
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
    #endregion
