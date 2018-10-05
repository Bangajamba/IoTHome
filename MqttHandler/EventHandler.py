from Event import Event
import os

class EventHandler():

    def __init__(self):
        self.events = []
        self.eventsTxt = "./events.txt"

    def createFile(self):
        if os.path.isfile(self.eventsTxt) == False:
            file = open(self.eventsTxt, 'w')
            file.write('{"Events": []}')
            file.close()
    


    def addEvent(self, src, des):
        event = Event(src, des)
        self.events.append(event)
        return event.getID()