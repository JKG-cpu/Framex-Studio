import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QPushButton

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 QGridLayout Example")

        # 1. Create a central container widget
        container = QWidget()
        self.setCentralWidget(container)

        # 2. Initialize the grid layout
        grid = QGridLayout()
        container.setLayout(grid)

        # 3. Add regular widgets (Row, Column)
        grid.addWidget(QPushButton("Button 0,0"), 0, 0)
        grid.addWidget(QPushButton("Button 0,1"), 0, 1)
        grid.addWidget(QPushButton("Button 1,0"), 1, 0)
        grid.addWidget(QPushButton("Button 1,1"), 1, 1)

        # 4. Add a spanning widget (Row 2, Column 0, spans 1 row, spans 2 columns)
        span_button = QPushButton("Spanning Button (Row 2, Col 0-1)")
        grid.addWidget(span_button, 2, 0, 1, 2)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
