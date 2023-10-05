

class Block:
    def __init__(self, id_:int, paramDict:dict , trainingTrialsCount:int, monitoredTrialsCount:int, currentTrial:int = 0) -> None:
        self.id_ = id_

        self.trainingTrialsCount = trainingTrialsCount
        self.monitoredTrialsCount = monitoredTrialsCount

        self.currentTrial = currentTrial

        self.paramDict = paramDict



    def toDict(self) -> dict:
        return {
                "id" : self.id_,
                "trainingTrialsCount" : self.trainingTrialsCount,
                "monitoredTrialsCount" : self.monitoredTrialsCount,
                "currentTrial": self.currentTrial,
                "params": self.paramDict
            }
    
    def __repr__(self) -> str:
        return str(self.toDict())

