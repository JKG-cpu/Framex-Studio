# =============================
# Main PySide6 Window (Layout)
# =============================
from PySide6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QPushButton,
    QWidget
)
import qdarktheme

__all__ = ["MainWindow"]

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Framex Studio Editor")
        self.resize(1600, 1000)

        self.is_dark = True

        layout = QVBoxLayout()
        self.toggle_btn = QPushButton("Switch to Light Mode")
        self.toggle_btn.clicked.connect(self.toggle_theme)
        layout.addWidget(self.toggle_btn)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def toggle_theme(self) -> None:
        if self.is_dark:
            qdarktheme.setup_theme("light")
            self.toggle_btn.setText("Switch to Dark Mode")
            self.is_dark = False

        else:
            qdarktheme.setup_theme("dark")
            self.toggle_btn.setText("Switch to Light Mode")
            self.is_dark = True
