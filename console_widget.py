import time

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QWidget, QScrollArea, QLabel, QVBoxLayout, QHBoxLayout, QDockWidget, QBoxLayout


from logger import logger, LogMessage

class LogMessageLabel(QLabel):
    def __init__(self, logMessage: LogMessage, parent: QWidget | None = ...) -> None:
        super().__init__(parent)
        self.setText(str(logMessage))



class ConsoleWidget(QScrollArea):
    def __init__(self, parent: QWidget | None = ...) -> None:
        super().__init__(parent)
        logger.newMessage.connect(self.addLogMessage)
        self.initUI()

    def initUI(self) -> None:

        self.widget = QWidget()                 # Widget that contains the collection of Vertical Box
        self.vbox = QVBoxLayout()               # The Vertical Box that contains the Horizontal Boxes of  labels and buttons
        self.vbox.addStretch()
        self.vbox.setDirection(QBoxLayout.BottomToTop)

        self.widget.setLayout(self.vbox)

        #Scroll Area Properties
        #self.setFixedSize(QSize(800, 600))
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setWidgetResizable(True)
        self.setWidget(self.widget)
        return
    
    def addDebugMessageLabel(self, logMessageLabel:LogMessageLabel) -> None:
        self.vbox.insertWidget(0, logMessageLabel)
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())

    def addLogMessage(self, logMessage:LogMessage):
        self.addDebugMessageLabel(LogMessageLabel(logMessage, self))




class DockConsoleWidget(QDockWidget):
    def __init__(self, parent: QWidget | None = ...) -> None:
        super().__init__(parent)
        self.consoleWidget = ConsoleWidget(self)
        self.setWidget(self.consoleWidget)
        self.setWindowTitle("Console")





