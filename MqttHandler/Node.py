import json
class Node():
    nrOfId = 0

    def __init__(self ,name, newID = -1, lastSend="", lastRecieve ="", triggerEvents = []):
        if newID == -1:
            self.ID = Node.nrOfId
            Node.nrOfId += 1
        else:
            self.ID = newID
            if Node.nrOfId <= newID:
                Node.nrOfId = newID + 1
        self.name = str(name)
        self.pubTopic = self.name + "/Out"
        self.subTopic = self.name + "/In"
        self.lastSendMsg = lastSend
        self.lastReceivedMsg = lastRecieve
        self.triggerEvents = triggerEvents

    def convertJson(self):
        jsonData = json.dumps(self.__dict__)
        return jsonData

    
