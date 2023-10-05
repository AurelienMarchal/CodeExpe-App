
from PyQt5.QtCore import QSize, Qt, QObject, QThread, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QDockWidget, 
    QTreeWidget, 
    QTreeWidgetItem, 
    QAbstractItemView, 
    QWidget, 
    QVBoxLayout, 
    QPushButton,
    )

import typing

from logger import logger
from main_widget import MainWidget
from participant_widget import ParticipantWidget

from experiment import Experiment
from settings import Settings
from experiment_parameter import ExperimentParameter
from participant import Participant
from block import Block



class ExplorerTreeWidgetItem(QTreeWidgetItem):

    def __init__(self, name:str):
        super(QTreeWidgetItem, self).__init__()
        self.name = name
        self.setText(0, self.name)


class ExplorerTreeWidget(QTreeWidget):
    openTabFromWidget = pyqtSignal(MainWidget)
    DISPLAY__METHODS = False
    
    def __init__(self, parent, experiment: Experiment=None):
        super(QTreeWidget, self).__init__(parent=parent)

        self.experiment:Experiment = None
        self.setExperiment(experiment)

        self.setColumnCount(1)

        self.setHeaderHidden(True)
        #self.setFixedSize(200, 200)

        self.itemPressed.connect(self.onItemPressed)
        self.itemDoubleClicked.connect(self.onItemDoubleClicked)

        #self.setDragDropMode(QAbstractItemView.DragOnly)

    def setExperiment(self, experiment: Experiment):
        self.experiment = experiment
        self.update()

    def update(self):
        self.clear()

    def onItemPressed(self, item:ExplorerTreeWidgetItem):
        pass

    def onItemDoubleClicked(self, item:ExplorerTreeWidgetItem):
        pass


class ExperimentParameterExplorerTreeWidgetItem(ExplorerTreeWidgetItem):
    def __init__(self, experimentParameter:ExperimentParameter):
        super().__init__(experimentParameter.name)
        #self.setIcon(0, QIcon("./Icons/settings-sliders.svg"))
        self.experimentParameter = experimentParameter
        self.generateChildren()
    
    def generateChildren(self):
        if self.experimentParameter is not None:
            for case in self.experimentParameter.caseList:
                self.addChild(ExperimentParameterExplorerTreeWidgetItemCaseExplorerTreeWidgetItem(case))


class ExperimentParameterExplorerTreeWidgetItemCaseExplorerTreeWidgetItem(ExplorerTreeWidgetItem):
    def __init__(self, experimentParameterCase:str):
        super().__init__(experimentParameterCase)
        self.setIcon(0, QIcon("./Icons/list-timeline.svg"))


class ExperimentParameterExplorerTreeWidget(ExplorerTreeWidget):
    def __init__(self, parent, experiment: Experiment):
        super().__init__(parent, experiment)

    def update(self):
        super().update()
        if self.experiment is not None:
            for experimentParameter in self.experiment.experimentParameterList:
                #logger.logInfo("ExperimentParameterExplorerTreeWidget", f"Adding {experimentParameter}")
                self.insertTopLevelItem(0, ExperimentParameterExplorerTreeWidgetItem(experimentParameter))

    def onItemPressed(self, item:ExplorerTreeWidgetItem):
        # Switch sur le type
        pass

    def onItemDoubleClicked(self, item:ExplorerTreeWidgetItem):
        # Switch sur le type
        pass


class ParticipantExplorerTreeWidgetItem(ExplorerTreeWidgetItem):
    def __init__(self, participant:Participant):
        super().__init__(f"Participant {participant.id_}")
        self.setIcon(0, QIcon("./Icons/user.svg"))
        self.participant:Participant = participant

class GroupParticipantExplorerTreeWidgetItem(ExplorerTreeWidgetItem):
    def __init__(self, groupNumber:int, participantList:typing.List[Participant]):
        super().__init__(f"Groupe {groupNumber}")
        self.groupNumber:int = groupNumber
        self.participantList:typing.List[Participant] = participantList
        self.generateChildren()
    
    def generateChildren(self) -> None:
        for participant in self.participantList:
            self.addChild(ParticipantExplorerTreeWidgetItem(participant))


class ExperimentExplorerTreeWidget(ExplorerTreeWidget):
    def __init__(self, parent, experiment: Experiment):
        super().__init__(parent, experiment)

    def update(self):
        super().update()
        if self.experiment is not None:
            for group in self.experiment.groupDict.keys():
                self.insertTopLevelItem(0, GroupParticipantExplorerTreeWidgetItem(group, self.experiment.groupDict[group]))

    def onItemPressed(self, item:ExplorerTreeWidgetItem):
        # Switch sur le type
        pass

    def onItemDoubleClicked(self, item:ExplorerTreeWidgetItem):
        # Switch sur le type
        pass


class ParticipantExplorerTreeWidget(ExplorerTreeWidget):
    def __init__(self, parent, experiment: Experiment):
        super().__init__(parent, experiment)

    def update(self):
        super().update()
        if self.experiment is not None:
            for group in self.experiment.groupDict.keys():
                self.insertTopLevelItem(0, GroupParticipantExplorerTreeWidgetItem(group, self.experiment.groupDict[group]))

    def onItemPressed(self, item:ExplorerTreeWidgetItem):
        # Switch sur le type
        pass

    def onItemDoubleClicked(self, item:ExplorerTreeWidgetItem):
        if isinstance(item, ParticipantExplorerTreeWidgetItem):
            self.openTabFromWidget.emit(ParticipantWidget(None, item.participant, self.experiment))

class SettingsExplorerTreeWidget(ExplorerTreeWidget):
    def __init__(self, parent, experiment: Experiment):
        super().__init__(parent, experiment)

    def update(self):
        super().update()

    def onItemPressed(self, item:ExplorerTreeWidgetItem):
        # Switch sur le type
        pass

    def onItemDoubleClicked(self, item:ExplorerTreeWidgetItem):
        # Switch sur le type
        pass





"""# Pas utilisé pour l'instant 
class ExplorerWidget(QWidget):
    def __init__(self, parent: typing.Optional['QWidget'] = ...) -> None:
        super().__init__(parent)
        self.explorerTree = ExplorerTreeWidget(self)
        self.initUI()

    def initUI(self):
        self.setLayout(QVBoxLayout(self))
        self.updateButton = QPushButton("Update", self)
        self.updateButton.setIcon(QIcon("./Icons/refresh.svg"))
        self.layout().addWidget(self.updateButton)
        self.layout().addWidget(self.explorerTree)
        self.updateButton.pressed.connect(self.explorerTree.update)


    def setExplorerTreeWidgetItem(self, explorerTreeWidgetItem : ExplorerTreeWidgetItem):
        self.explorerTree = explorerTreeWidgetItem
        self.initUI()
"""

class Explorer(QDockWidget):
    def __init__(self, parent):
        super(QDockWidget, self).__init__(parent=parent)
        self.setWindowTitle('Explorer')
        self.explorerTreeWidget:ExplorerTreeWidget = None
        #self.setExplorerTreeWidget(ExplorerTreeWidget(self))
    
    def setExplorerTreeWidget(self, explorerTreeWidget : ExplorerTreeWidget):
        self.explorerTreeWidget = explorerTreeWidget
        self.explorerTreeWidget.update()
        self.setWidget(self.explorerTreeWidget)