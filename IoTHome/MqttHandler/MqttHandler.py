import paho.mqtt.client as mqtt
from threading import Thread
from NodeHandler import NodeHandler

import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('ip', action='store', default='127.0.0.1', type=str, help='ipaddres to connect')

args = parser.parse_args()

class MqttHandler():
    def __init__(self):

        self.nodeHandler = NodeHandler()

        # Mqtt
        self.listenClient = mqtt.Client(userdata=self)
        self.listenClient.on_connect = on_connect
        
        self.listenClient.on_message = on_message
        self.listenClient.connect(args.ip, 1883, 60)

        self.t = Thread(target = self.listenClient.loop_forever)
        self.t.daemon = True
        self.t.start()

        self.client = mqtt.Client()
        self.client.connect(args.ip, 1883, 60)
        
    
    def changeData(self, msg):
        #arr = msg.topic.split('/')
        #if(len(arr) > 0):
        index = self.nodeHandler.findByNameNode(msg.topic)
        self.nodeHandler.nodes[index].lastMsg = msg.payload.decode()
        print(self.nodeHandler.nodes[index].lastMsg)
    

    def sendPayload(self, name, payload):
        self.client.publish(name, payload)





def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("#")
    
def on_message(client, userdata, msg):
    userdata.changeData(msg)


if __name__ == "__main__":
    m = MqttHandler()
    
    #print("write 'stop' to end")
    #exitCommand = ""
    while(True):
        #exitCommand = input()
        pass
        
    
    print("Slutar While")

# C:\Users\KCHBBH\Desktop\IoTHome