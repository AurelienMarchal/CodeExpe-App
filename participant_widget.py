import typing
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize, Qt, QObject, pyqtSignal
from PyQt5.QtWidgets import (
    QPushButton, 
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QTabWidget, 
    QWidget, 
    QLabel,
    QComboBox,
    QSpacerItem,
    QSizePolicy
)   

from logger import logger

from Networking.client import client

from participant import Participant
from block import Block
from experiment import Experiment
from experiment_parameter import ExperimentParameter
from main_widget import MainWidget


class ParticipantWidget(MainWidget):
    def __init__(self, parent: QWidget | None, participant:Participant, experiment:Experiment) -> None:
        super().__init__(parent, f"Participant {participant.id_}")

        self.participant = participant
        self.experiment = experiment
        self.currentBlockId = 0
        self.initUI()


    def initUI(self):

        self.setLayout(QVBoxLayout(self))

        self.participantIdLabel = QLabel(f"Participant {self.participant.id_}")
        font = self.font()
        font.setPointSize(32)
        font.setBold(True)
        self.participantIdLabel.setFont(font)

        self.sendManualBlockDataButton = QPushButton("Send block data")
        self.sendManualBlockDataButton.clicked.connect(self.onSendManualBlockDataButtonClicked)

        self.manualBlockDataSelectionWidget = ManualBlockDataSelectionWidget(self, self.experiment)

        self.layout().addWidget(self.participantIdLabel)
        self.layout().addWidget(self.manualBlockDataSelectionWidget)
        self.layout().addWidget(self.sendManualBlockDataButton)
        self.layout().addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        



    def onSendManualBlockDataButtonClicked(self):
        #block = Block({"TI": "Joystick", "Visualization": "PerspectiveWall", "Task": "Locate"}, 2, 3, 0)
        
        if self.manualBlockDataSelectionWidget.getParameterDict()["Task"] == "Pattern":
        
            block = Block(self.currentBlockId, self.manualBlockDataSelectionWidget.getParameterDict(), 4, 8, 0)

        elif self.manualBlockDataSelectionWidget.getParameterDict()["Task"] == "Locate":

            block = Block(self.currentBlockId, self.manualBlockDataSelectionWidget.getParameterDict(), 4, 12, 0)

        self.currentBlockId += 1
        client.emit("user", self.participant.toDict())
        client.emit("block", block.toDict())
        
        
class ManualBlockDataSelectionWidget(QWidget):
    def __init__(self, parent: QWidget, experiment : Experiment) -> None:
        super().__init__(parent)
        self.experiment = experiment
        self.comboBoxParameterList:typing.List[ComboBoxParameter] = []
        self.initUI()


    def initUI(self):

        self.setLayout(QVBoxLayout())

        self.comboBoxLayoutWidget = QWidget(self)
        self.comboBoxLayoutWidget.setLayout(QGridLayout(self))

        for ind, experimentParameter in enumerate(self.experiment.experimentParameterList):
            comboBoxParameter = ComboBoxParameter(self, experimentParameter)
            self.comboBoxParameterList.append(comboBoxParameter)
            self.comboBoxLayoutWidget.layout().addWidget(QLabel(experimentParameter.name), 0, ind)
            self.comboBoxLayoutWidget.layout().addWidget(comboBoxParameter, 1, ind)

        self.layout().addWidget(QLabel("Manual Parameter Selection"))
        self.layout().addWidget(self.comboBoxLayoutWidget)
        

    
    def getParameterDict(self) -> dict:
        returnDict = {}
        for comboBoxParameter in self.comboBoxParameterList:
            returnDict[comboBoxParameter.experimentParameter.name] = comboBoxParameter.currentText()
        
        return returnDict



class ComboBoxParameter(QComboBox):
    def __init__(self, parent: QWidget | None, experimentParameter: ExperimentParameter) -> None:
        super().__init__(parent)
        self.experimentParameter = experimentParameter
        self.addItems(self.experimentParameter.caseList)










