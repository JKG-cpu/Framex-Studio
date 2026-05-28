# ===========
# Entry Point
# ===========
from PySide6.QtWidgets import QApplication
import qdarktheme

from editor import *

if __name__ == "__main__":
    app = QApplication()

    qdarktheme.setup_theme("dark")

    window = MainWindow()
    window.show()

    exit(app.exec())