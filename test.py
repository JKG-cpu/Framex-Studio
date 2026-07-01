import sys
import qdarktheme
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMenu,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QLabel,
)
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt, QPoint


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dynamic Context Menu")
        self.resize(400, 300)

        # Main Layout Setup
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Dummy widgets to test right-clicks
        self.btn = QPushButton("Right-click Me!")
        self.lbl = QLabel("Or Right-click Me!", alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.btn)
        layout.addWidget(self.lbl)

        # 1. Enable custom context menus on the main window
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def show_context_menu(self, pos: QPoint):
        menu = QMenu(self)

        # 2. Find exactly which widget sits at the click position
        target_widget = self.childAt(pos)

        # 3. Dynamically populate the menu based on the widget type or reference
        if target_widget == self.btn:
            act = QAction("Button Specific Action", self)
            act.triggered.connect(lambda: print("Clicked button menu option"))
            menu.addAction(act)

        elif target_widget == self.lbl:
            act = QAction("Label Specific Action", self)
            act.triggered.connect(lambda: print("Clicked label menu option"))
            menu.addAction(act)

        else:
            # Fallback menu for clicking empty space inside the window
            act = QAction("General Window Action", self)
            menu.addAction(act)

        # 4. Display the menu
        menu.exec(self.mapToGlobal(pos))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    qdarktheme.setup_theme("dark")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
