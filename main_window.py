import sys

from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize, Qt, QObject, QThread, pyqtSignal
from PyQt5.QtWidgets import (
    QApplication, 
    QMainWindow, 
    QPushButton, 
    QTableView, 
    QVBoxLayout, 
    QTabWidget, 
    QStatusBar, 
    QToolBar, 
    QAction, 
    QWidget, 
    QLabel,
) 

from console_widget import ConsoleWidget, DockConsoleWidget
from explorer_widget import Explorer, ExperimentParameterExplorerTreeWidget, ExperimentExplorerTreeWidget, ParticipantExplorerTreeWidget, SettingsExplorerTreeWidget
from main_widget import MainWidget

from logger import logger
from Networking.receiver import ReceiverWorker
from Networking.client import client

from experiment import Experiment, createTestExpe

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.experiment:Experiment = None

        self.setWindowTitle("Application Expe")

        self.tabs = QTabWidget(self)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(lambda index: self.tabs.removeTab(index))
        self.setCentralWidget(self.tabs)

        self.explorer = Explorer(self)
        self.addDockWidget(Qt.DockWidgetArea(1), self.explorer)

        self.experimentParameterExplorerTreeWidget: ExperimentParameterExplorerTreeWidget = ExperimentParameterExplorerTreeWidget(self.explorer, None)
        self.experimentExplorerTreeWidget: ExperimentExplorerTreeWidget = ExperimentExplorerTreeWidget(self.explorer, None)
        self.participantExplorerTreeWidget: ParticipantExplorerTreeWidget = ParticipantExplorerTreeWidget(self.explorer, None)
        self.settingsExplorerTreeWidget: SettingsExplorerTreeWidget = SettingsExplorerTreeWidget(self.explorer, None)
        self.participantExplorerTreeWidget.openTabFromWidget.connect(self.addTabFromMainWidget)

        self.dockConsoleWidget = DockConsoleWidget(self)
        self.addDockWidget(Qt.DockWidgetArea(8), self.dockConsoleWidget)
        
        self.setDockOptions(QMainWindow.AnimatedDocks | QMainWindow.AllowNestedDocks)

        self.createStatusBar()
        self.setConnectionStatus(client.isConnected)

        self.createToolBar()

        self.setGeometry(0, 0, 1800, 1100)

        #Test
        self.setExperiment(createTestExpe())

    def setExperiment(self, experiment: Experiment):
        self.experiment = experiment
        self.setWindowTitle(self.experiment.name)
        self.experimentParameterExplorerTreeWidget.setExperiment(experiment)
        self.experimentExplorerTreeWidget.setExperiment(experiment)
        self.participantExplorerTreeWidget.setExperiment(experiment)
        self.settingsExplorerTreeWidget.setExperiment(experiment)


    def createToolBar(self):
        self.sceneToolbar = QToolBar("Menu")
        self.sceneToolbar.setIconSize(QSize(32,32))
        self.sceneToolbar.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.createToolBarActions()

        self.sceneToolbar.addAction(self.experimentAction)
        self.sceneToolbar.addSeparator()
        self.sceneToolbar.addAction(self.participantAction)
        self.sceneToolbar.addSeparator()
        self.sceneToolbar.addAction(self.parametersAction)
        self.sceneToolbar.addSeparator()
        self.sceneToolbar.addAction(self.settingsAction)

        self.addToolBar(Qt.LeftToolBarArea, self.sceneToolbar)

    def createToolBarActions(self):
        experimentIcon = QIcon("./Icons/play.svg")
        self.experimentAction = QAction(experimentIcon, "Fill Color", self)
        self.experimentAction.setToolTip("Experiment")
        self.experimentAction.triggered.connect(self.onRunActionTriggered)
        #self.experimentAction.setCheckable(True)

        participantIcon = QIcon("./Icons/users-alt.svg")
        self.participantAction = QAction(participantIcon, "Fill Color", self)
        self.participantAction.setToolTip("Participants")
        self.participantAction.triggered.connect(self.onParticipantActionTriggered)
        #self.participantAction.setCheckable(True)

        parametersIcon = QIcon("./Icons/settings-sliders.svg")
        self.parametersAction = QAction(parametersIcon, "Fill Color", self)
        self.parametersAction.setToolTip("Parameters")
        self.parametersAction.triggered.connect(self.onParametersActionTriggered)
        #self.parametersAction.setCheckable(True)

        settingsIcon = QIcon("./Icons/settings.svg")
        self.settingsAction = QAction(settingsIcon, "Fill Color", self)
        self.settingsAction.setToolTip("Settings")
        self.settingsAction.triggered.connect(self.onSettingsActionTriggered)
        #self.settingsAction.setCheckable(True)

    def createStatusBar(self):

        self.setStatusBar(QStatusBar(self))
        self.connectionButtonStatusBar = QPushButton("Connect", self)
        self.linkIconLabelStatusBar = QLabel()
        self.connectedLabelStatusBar = QLabel()
        self.connectedLabelStatusBar.setFixedWidth(100)
        self.connectedLabelStatusBar.setAlignment(Qt.AlignCenter)

        self.statusBar().addPermanentWidget(self.linkIconLabelStatusBar)
        self.statusBar().addPermanentWidget(self.connectedLabelStatusBar)
        self.statusBar().addPermanentWidget(self.connectionButtonStatusBar)

        self.connectionButtonStatusBar.clicked.connect(self.tryToConnect)

        client.connectionStatusChanged.connect(self.setConnectionStatus)

    def setConnectionStatus(self, connectionStatus:bool):
        if connectionStatus:
            self.connectionButtonStatusBar.setDisabled(True)
            linkIconPixMapStatusBar = QPixmap("./icons/link.svg").scaledToHeight(self.statusBar().height()-16)
            self.linkIconLabelStatusBar.setPixmap(linkIconPixMapStatusBar)
            self.connectedLabelStatusBar.setText("Connected")
        
        else:
            self.connectionButtonStatusBar.setDisabled(False)
            linkIconPixMapStatusBar = QPixmap("./icons/link-slash.svg").scaledToHeight(self.statusBar().height()-16)
            self.linkIconLabelStatusBar.setPixmap(linkIconPixMapStatusBar)
            self.connectedLabelStatusBar.setText("Not connected")


    def tryToConnect(self):
        client.tryToConnect()
        self.startReceiverThread()

    def startReceiverThread(self):
        self.thread = QThread()
        self.receiverWorker = ReceiverWorker(client)
        self.receiverWorker.moveToThread(self.thread)
        self.thread.started.connect(self.receiverWorker.run)
        self.receiverWorker.finished.connect(self.thread.quit)
        self.receiverWorker.finished.connect(self.receiverWorker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.receiverWorker.sendData.connect(self.handleNetworkingData)

        self.thread.start()

        self.thread.finished.connect(
            lambda: self.setConnectionStatus(False)
        )


    def handleNetworkingData(self, data:str):
        pass
        #logger.logInfo("NetworkingData", f"Received {data}")

    def addTabFromMainWidget(self, widget:MainWidget):
        self.tabs.addTab(widget, widget.tabName)


    def onRunActionTriggered(self):
        self.explorer.setExplorerTreeWidget(self.experimentExplorerTreeWidget)
        self.explorer.setWindowTitle("Explorer (Experiment)")
    
    def onParticipantActionTriggered(self):
        self.explorer.setExplorerTreeWidget(self.participantExplorerTreeWidget)
        self.explorer.setWindowTitle("Explorer (Participants)")

    def onParametersActionTriggered(self):
        self.explorer.setExplorerTreeWidget(self.experimentParameterExplorerTreeWidget)
        self.explorer.setWindowTitle("Explorer (Parameters)")


    def onSettingsActionTriggered(self):
        self.explorer.setExplorerTreeWidget(self.settingsExplorerTreeWidget)
        self.explorer.setWindowTitle("Explorer (Settings)")

    def closeEvent(self,event):
        #print("Saving before closing")
        #if self.project is not None:
        #    self.project.save()
        logger.logInfo("CloseEvent", "Closing")
        event.accept()
        #result = QMessageBox.question(self,
        #              "Confirm Exit...",
        #              "Are you sure you want to exit ?",
        #              QMessageBox.Yes| QMessageBox.No)
        #event.ignore()
        #
        #if result == QMessageBox.Yes:
        #    event.accept()

        #Force Exit
        sys.exit()


if __name__ == "__main__":

    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())