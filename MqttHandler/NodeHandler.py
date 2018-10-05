from Node import Node

class NodeHandler():
    def __init__(self):
        self.nodes = []
        #self.add("Pir")
        print(self.nodes)



    def add(self, newNode):
        self.nodes.append(newNode)

    def addTriggersToNodes(self, src, eventID):
        #size = len(self.nodes)
        '''for node in self.nodes:
            for trigger in src:
                if trigger['type'] == "Node":
                    if trigger['nodeId'] == node.name:
                        node.triggerEvents.append(eventID)
        '''
        for trigger in src:
            print(trigger)
            if trigger['type'] == "Node":
                index = self.findByNameNode(trigger['nodeId'])
                if index != -1:
                    self.nodes[index].triggerEvents.append(eventID)
                    print(trigger['nodeId'])
                    print(self.nodes[index].name)

    # Find node by name, return -1 if not find, return index position otherwise 
    def findByNameNode(self, name):
        i = 0
        find = False

        while(find == False and i < len(self.nodes)):
            if self.nodes[i].name == name:
                find = True
            else:
                i += 1

        if find == False:
            i = -1

        return i

    def convertJson(self):
        result =""
        lenght = len(self.nodes)
        if lenght > 0:
            
            for i in range(lenght):
                result += self.nodes[i].convertJson()
                if i < lenght - 1:
                    result += ", "
            

        return result

    def addEventTriggers(self, src):
        pass

