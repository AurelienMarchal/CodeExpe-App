from PyQt5.QtCore import Qt, QObject, QThread, pyqtSignal


import socket
import json

from .client import Client
from logger import logger


splitter = "[{//V//}]"


class ReceiverWorker(QObject):
    finished = pyqtSignal()
    sendData = pyqtSignal(bytes)

    def __init__(self, client:Client) -> None:
        super().__init__(None)
        self.client:Client = client

    def run(self):

        global splitter

        try:
            while True:
                temp = self.client.sock.recv(1024)
                if temp:
                    data = temp
                    self.sendData.emit(data)
                    try:
                        strData = bytes.decode(data, 'utf-8')
                        strData = strData.split(splitter)[0]
                        dictData = json.loads(strData)
                        
                        for key in dictData.keys():
                            if key in dir(self):
                                if(callable(getattr(self, key))):
                                    getattr(self, key)(dictData[key])

                    except Exception as e:
                        logger.logError("ReceiverThread", str(e))


        except Exception as e:
            logger.logError("ReceiverThread", str(e))

        finally:
            self.finished.emit()
            self.client.sock.close()


    def connect(self, data):
        logger.logInfo("ConnectChannel", data)
        self.client.setIsConnected(True)
        #sending client info
        self.client.emit("client_info", {"role" : self.client.role, "name": self.client.name})


    def disconnect(self, data):
        self.client.setIsConnected(False)
        logger.logInfo("DisconnectChannel", data)
