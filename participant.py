import typing

LAST_ID = -1

class Participant:
    
    def __init__(self, id_:int=None, group:int = None) -> None:
        global LAST_ID
        self.id_:int = id_
        if self.id_ is None :
            LAST_ID += 1
            self.id_ = LAST_ID 

        self.group: int = group


    def toDict(self) -> dict:
        return {"id": str(self.id_), "group": self.group}




