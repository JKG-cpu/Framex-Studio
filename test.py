import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout

class FullMouseDetectorWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 Mouse & Scroll Tracker")
        self.resize(400, 300)
        
        # UI Setup
        layout = QVBoxLayout(self)
        self.click_label = QLabel("Click somewhere inside")
        self.scroll_label = QLabel("Scroll your wheel/trackpad")
        self.move_label = QLabel("Move the mouse")
        
        for lbl in (self.click_label, self.scroll_label, self.move_label):
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(lbl)
            
        # Enable tracking without needing to click down
        self.setMouseTracking(True)

    def mousePressEvent(self, event):
        # Detect specific button clicked
        button = event.button()
        if button == Qt.MouseButton.LeftButton:
            btn_text = "Left Button 🔴"
        elif button == Qt.MouseButton.RightButton:
            btn_text = "Right Button 🔵"
        elif button == Qt.MouseButton.MiddleButton:
            btn_text = "Middle Button / Wheel 🟢"
        else:
            btn_text = "Other Button"
            
        self.click_label.setText(f"Clicked: {btn_text}")
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        # Track coordinates
        pos = event.position()
        self.move_label.setText(f"Position: X={int(pos.x())}, Y={int(pos.y())}")
        super().mouseMoveEvent(event)

    def wheelEvent(self, event):
        # angleDelta provides both X (horizontal) and Y (vertical) streams
        delta = event.angleDelta()
        y_steps = delta.y()
        x_steps = delta.x()
        
        status = []
        
        # Vertical scrolling (Up / Down)
        if y_steps > 0:
            status.append("Vertical: Up ⬆️")
        elif y_steps < 0:
            status.append("Vertical: Down ⬇️")
            
        # Horizontal scrolling (Left / Right - e.g., trackpad swipe or shift+wheel)
        if x_steps > 0:
            status.append("Horizontal: Right ➡️")
        elif x_steps < 0:
            status.append("Horizontal: Left ⬅️")
            
        if status:
            self.scroll_label.setText(" | ".join(status))
        
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FullMouseDetectorWidget()
    window.show()
    sys.exit(app.exec())
