from Broker import Broker
from Node import Node
import os
import json

class IoTPlatform():
    def __init__(self, ip):
        self.nodesTxt = "./nodes.txt"
        self.broker = Broker(ip)
        self.createFile()
        self.loadFromFile()
        
    
    def createFile(self):
        if os.path.isfile(self.nodesTxt) == False:
            file = open(self.nodesTxt, 'w')
            file.write('{"MQTT": []}')
            file.close()
    
    def saveToFile(self):
        file = open(self.nodesTxt, "w")

        fileData = "{"

        tempString = self.broker.nodeHandler.convertJson()
        if tempString == "":
            fileData += '"MQTT": []'
        else:
            fileData += '"MQTT":[' + tempString + "]"

        fileData += "}"
        file.write(fileData)
        file.close()

    
    def loadFromFile(self):
        file = json.load(open(self.nodesTxt))
        for mqtt in file['MQTT']:
            self.broker.nodeHandler.add(Node(mqtt['name'], mqtt['ID'], mqtt['lastSendMsg'], mqtt['lastReceivedMsg'], mqtt['triggerEvents']))

    def addNodeAndSaveFile(self, name):
        self.broker.nodeHandler.add(Node(name))
        self.saveToFile()
        pass

    def nodeSendPayload(self, name, payload):
        self.broker.sendPayload(name, payload)

    def getNodes(self):
        return  '{"MQTT":[' + self.broker.nodeHandler.convertJson() + "]}"

    def addTriggersToNodesAndSaveFile(self, src, eventID):
        self.broker.nodeHandler.addTriggersToNodes(src, eventID)
        self.saveToFile()