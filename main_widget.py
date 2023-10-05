from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize, Qt, QObject, QThread, pyqtSignal
from PyQt5.QtWidgets import (
    QWidget, 
    QLabel,
    
)   




class MainWidget(QWidget):
    def __init__(self, parent: QWidget | None, tabName:str) -> None:
        super().__init__(parent)

        self.tabName = tabName



