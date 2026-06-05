# ===========
# Entry Point
# ===========
import qdarktheme
from PySide6.QtWidgets import QApplication
from os import system, name

from src.editor import *

def cc():
    system("cls" if name == "nt" else "clear")

if __name__ == "__main__":
    app = QApplication()

    qdarktheme.setup_theme("dark")

    with open("styling.qss") as f:
        app.setStyleSheet(app.styleSheet() + f.read())

    window = MainWindow(
        "test_game_folder"
    )

    window.show()

    exit_code = app.exec()
    cc()
    exit(exit_code)