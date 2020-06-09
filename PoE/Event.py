class Event():
    nrOfId = 0
    def __init__(self, src, des, newID = -1):
        self.src = src
        self.des = des
        if newID == -1:
            self.ID = Event.nrOfId
            Event.nrOfId += 1
        else:
            self.ID = newID
            if Event.nrOfId <= newID:
                Event.nrOfId = newID + 1

    def getID(self):
        return self.ID    