from Node import Node

class NodeHandler():
    def __init__(self):
        self.nodes = []
        self.add("/home/bedroom/", "pir")
        print(self.nodes)



    def add(self, parentName, name):
        self.nodes.append(Node(name))

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


