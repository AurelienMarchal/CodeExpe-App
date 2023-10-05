import typing 


class ExperimentParameter:
    def __init__(self, name:str, caseList: typing.List[str] = []) -> None:
        self.name:str = name
        self.caseList = caseList