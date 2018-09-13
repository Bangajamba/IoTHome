class Node():
    nrOfId = 0

    def __init__(self ,name):
        self.ID = Node.nrOfId
        Node.nrOfId += 1
        self.name = name
        self.payload = ""
        self.lastMsg = ""

    
