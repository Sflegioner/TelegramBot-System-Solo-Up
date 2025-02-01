
class DailyTask:
    id:int
    complated: bool
    description:str
    time_of_creation: str

    def __init__(self,id,description):
        self.id = id
        self.complated = False
        self.description = description
        self.time_of_creation = ""