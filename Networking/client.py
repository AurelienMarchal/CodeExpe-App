import socket
import json

from PyQt5.QtCore import Qt, QObject, QThread, pyqtSignal

from logger import logger

#host = "192.168.0.101"
host = "localhost"
port = 5000

splitter = "[{//V//}]"


class Client(QObject):
    role = "application"
    name = "Application Expe"

    connectionStatusChanged = pyqtSignal(bool)

    def __init__(self, parent:QObject = None) -> None:
        super().__init__(parent)
        self.sock: socket.socket = None
        self.isConnected = False

    def setIsConnected(self, isConnected:bool):
        self.isConnected = isConnected
        self.connectionStatusChanged.emit(self.isConnected)
    
    def tryToConnect(self):
        server_addr = (host, port)

        logger.logInfo("Client", f"Starting connection to {server_addr}")

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #self.sock.setblocking(False)
            self.sock.connect_ex(server_addr)

        except Exception as e:
            logger.logError("Client", str(e))


    def emit(self, channel:str, data:object):
        global splitter
        tempdata = {}
        tempdata[channel] = data
        tempdata['identify'] = channel
        message = json.dumps(tempdata) + splitter

        logger.logInfo("Client", f"Sending : {message}")

        try:
            self.sock.send(message.encode('utf-8'))

        except Exception as e:
            logger.logError("Client", str(e))


client = Client()