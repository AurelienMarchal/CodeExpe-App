from PyQt5.QtCore import Qt, QObject, QThread, pyqtSignal
import typing
import time


class LogMessage:
    def __init__(self, source:str, message:str) -> None:
        self.source :str = source
        self.message:str = message
        t = time.localtime()
        self.createTime = time.strftime("%H:%M:%S", t)
    
    def __repr__(self) -> str:
        return f"{ self.createTime} [{self.source}] : {self.message}"

    def __str__(self) -> str:
        return self.__repr__()

class InfoLogMessage(LogMessage):
    def __init__(self, source: str, message: str) -> None:
        super().__init__(source, message)

class ErrorLogMessage(LogMessage):
    def __init__(self, source: str, message: str) -> None:
        super().__init__(source, message)

class WarningLogMessage(LogMessage):
    def __init__(self, source: str, message: str) -> None:
        super().__init__(source, message)


class Logger(QObject):
    newMessage = pyqtSignal(LogMessage)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.logMessageList:typing.List[LogMessage] = []

    def logInfo(self, source:str, message:str):
        newMessage = InfoLogMessage(source, message)
        self.addNewMessage(newMessage)

    def logWarning(self, source:str, message:str):
        newMessage = WarningLogMessage(source, message)
        self.addNewMessage(newMessage)

    def logError(self, source:str, message:str):
        newMessage = ErrorLogMessage(source, message)
        self.addNewMessage(newMessage)

    def addNewMessage(self, logMessage:LogMessage):
        self.logMessageList.append(logMessage)
        self.newMessage.emit(logMessage)
        print(logMessage)        


logger = Logger()