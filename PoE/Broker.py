from NodeHandler import NodeHandler
from MqttHandler import MqttHandler
from InfluxDB import InfluxDB

import logging
import socket 

class Broker():
    def __init__(self, ip):
        self.ip = ip
        # TODO not logging .error type for now, add in config 
        logging.basicConfig(level=logging.INFO)
        logging.info(self.ip)
        logging.info(socket.gethostbyname(socket.gethostname()))

        # Node Handler
        self.nodeHandler = NodeHandler()

        # MqttCommuncation
        self.mqttHandler = MqttHandler(self.ip, self) 
        
        #InfluxDB
        self.influxClient = InfluxDB(self.ip)
        
    def on_message(self, msg):
        result = None
        try:
            #TODO CHANGE BACK MSG
            msgs = msg.payload.decode().split(",")
            size = len(msgs)
            if size > 1 and size % 2 == 0:
                arr = []
                index = 0
                while index < size:
                    temp = {}
                    temp['key'] = msgs[index]
                    temp['value'] = self.influxClient.returnValue(msgs[(index+1)])
                    arr.append(temp)
                    index += 2
                result = arr
                
        except Exception as e:
            print(e)
            logging.info(str(e))

        topic = msg.topic
        payloads = ""
        if result is not None:
            payloads = result
        else:
            payloads = [msg.payload.decode()]

        self.influxClient.sendToInfluxDB(topic, payloads)

        # /bedroom/Pir/Out
        #name = msg.topic.replace("/In", "")
        #index = self.nodeHandler.findByNameNode(name)
        #if index != -1:
        #self.nodeHandler.nodes[index].lastReceivedMsg = msg.payload.decode()

    def sendPayload(self, name, payload):
        index = self.nodeHandler.findByNameNode(name)
        pubTopic = self.nodeHandler.nodes[index].pubTopic
        self.nodeHandler.nodes[index].lastSendMsg = payload
        self.mqttHandler.client.publish(pubTopic, payload)

if __name__ == "__main__":
    b = Broker("127.0.0.1")
    
    #print("write 'stop' to end")
    #exitCommand = ""
    while(True):
        #exitCommand = input()
        pass
        
    
    print("Slutar While")

# C:\Users\KCHBBH\Desktop\IoTHome