import sys
from PySide6.QtCore import Slot
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PySide6 Interactive Example")
        self.resize(400, 200)

        self.label = QLabel("Enter your name below:")
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type something here...")
        
        self.button = QPushButton("Greet Me!")

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.input_field)
        layout.addWidget(self.button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.button.clicked.connect(self.on_button_click)

    @Slot()
    def on_button_click(self):
        """Slot function triggered when the button is clicked."""
        user_text = self.input_field.text().strip()
        if user_text:
            self.label.setText(f"Hello, {user_text}!")
        else:
            self.label.setText("Please type a name first!")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
