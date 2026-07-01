# ========================
# Base Panel
# ========================
from PySide6.QtWidgets import QWidget
from PySide6 import QtCore

__all__ = ["Panel"]


class Panel(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__()
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.setContentsMargins(8, 8, 8, 8)
