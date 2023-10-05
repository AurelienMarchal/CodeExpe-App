import typing 

import itertools

from logger import logger

from settings import Settings
from experiment_parameter import ExperimentParameter
from participant import Participant
from block import Block


# Main class
class Experiment:
    def __init__(
                self,
                name:str,
                settings:Settings, 
                experimentParameterList:typing.List[ExperimentParameter] = [],
                participantList:typing.List[Participant] = [],
                blockList:typing.List[Block] = []
                ) -> None:
        
        self.name = name
        self.settings:Settings = settings
        self.experimentParameterList:typing.List[ExperimentParameter] = experimentParameterList
        self.participantList:typing.List[Participant] = participantList
        self.blockList:typing.List[Block] = blockList
        self.groupDict = {}
        self.updateGroupDict()

    def generateBlocks(self):
        
        casesList = [experimentParameter.caseList for experimentParameter in self.experimentParameterList]

        combinaisonList = list(itertools.product(*tuple(casesList)))

        logger.logInfo("GenerateBlocks", f"Generating {len(combinaisonList)} blocks")

        experimentParameterNameList = [experimentParameter.name for experimentParameter in self.experimentParameterList]
    

        self.blockList = []

        for combinaison in combinaisonList:

            paramDict = {}

            for case, experimentParameterName in zip(combinaison, experimentParameterNameList):
                paramDict[experimentParameterName] = case
            
            newBlock = Block(paramDict, self.settings.trainingTrialsCount, self.settings.monitoredTrialsCount)
            self.blockList.append(newBlock)

    def updateGroupDict(self):
        self.groupDict = {}
        for participant in self.participantList:
            if participant.group not in self.groupDict:
                self.groupDict[participant.group] = []
            self.groupDict[participant.group].append(participant)

def createTestExpe() -> Experiment :
    par1 = Participant(group=0)
    par2 = Participant(group=1)
    par3 = Participant(group=1)
    par4 = Participant(group=1)
    par5 = Participant(group=1)
    par6 = Participant(group=2)
    par7 = Participant(group=2)
    par8 = Participant(group=2)
    par9 = Participant(group=2)
    par10 = Participant(group=3)
    par11 = Participant(group=3)
    par12 = Participant(group=3)
    par13 = Participant(group=3)



    expeParam1 = ExperimentParameter("TI", ["AB", "OrthozoomDepthJoystick", "OrthozoomDepth", "OrthozoomJoystickControllerDist", "Slider"])
    expeParam2 = ExperimentParameter("Visualization", [ "PerspectiveWall", "NoTimeline", "Helice"])
    expeParam3 = ExperimentParameter("Task", ["Locate", "Pattern"])

    expe = Experiment("Test Expe", Settings(), [expeParam1, expeParam2, expeParam3], [par1, par2, par3, par4, par5, par6, par7, par8, par9, par10, par11, par12,par13])

    #expe.generateBlocks()

    return expe


        
if __name__ == "__main__":
    expe = createTestExpe()

    expe.generateBlocks()

    print(expe.blockList)

