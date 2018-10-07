from NodeHandler import NodeHandler
from threading import Thread
from influxdb import InfluxDBClient

import paho.mqtt.client as mqtt
import datetime
import logging
import socket 



class MqttHandler():
    def __init__(self, ip):
        self.ip = ip
        logging.basicConfig(level=logging.INFO)
        logging.info(self.ip)
        logging.info(socket.gethostbyname(socket.gethostname()))

        # Node Handler
        self.nodeHandler = NodeHandler()

        # MqttCommuncation
        self.mqttConnected = False #not in use
        self.connectMqtt()
        

        #InfluxDB
        self.inflexConnected = False #not in use
        self.connectInflexDB() 
        


    def connectMqtt(self):
        try:
            # MqttListener used for receive incoming message(subscribe)
            self.listenClient = mqtt.Client(userdata=self)
            self.listenClient.on_connect = on_connect
            
            self.listenClient.on_message = on_message
            self.listenClient.connect(self.ip, 1883, 60)

            self.t = Thread(target = self.listenClient.loop_forever)
            self.t.daemon = True
            self.t.start()
            logging.info("MqttServer Done")

            # MqttClient used for send message(publish)
            self.client = mqtt.Client()
            self.client.connect(self.ip, 1883, 60)
            self.mqttConnected = True
            logging.info("MqttClient Done")
        except:
            logging.info("Failed Connect Mqtt")
        
    def connectInflexDB(self):
        try:
            self.influx_client = InfluxDBClient(self.ip, 8086, username='admin', password='secretpassword',database='iot')
            self.inflexConnected = True
        except:
            logging.info("Failed Connect InflexDB")

        
    def sendToInfluxDB(self, topic, msg):
        current_time = datetime.datetime.utcnow().isoformat()

        result = {}
        if len(msg) > 1:
            for m in msg:
                result[m['key']] = m['value']
        elif len(msg) == 1:
            result['PAYLOADSTRING'] = msg[1] 
        else:
            raise "FAIL"

        json_body = [
            {
                "measurement": str(topic),
                "tags": {},
                "time": current_time,
                "fields": result
            }
        ]
        try:
            logging.info(json_body)
            self.influx_client.write_points(json_body)
        except Exception as e:
            logging.info("fail write to influx:" + str(e))
    
    def returnValue(self, strValue):
        result = strValue
        try:
            result = float(strValue)
            if result.is_integer():
                result = int(strValue)
        except:
            try:
                result = int(strValue)
            except:
                
                try:
                    print(result)
                    if result == "True" or result == "true":
                        result = 1
                    elif result == "False" or result == "false":
                        result = 0
                except:
                    pass    
        return result

    #key,value,key2,value2
    #else string
    def changeData(self, msg):
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
                    temp['value'] = self.returnValue(msgs[(index+1)])
                    arr.append(temp)
                    index += 2
                result = arr
                
        except Exception as e:
            print(e)

        topic = msg.topic
        payloads = ""
        if result is not None:
            payloads = result
        else:
            payloads = [msg.payload.decode()]
        
        self.sendToInfluxDB(topic, payloads)

        # /bedroom/Pir/Out
        #name = msg.topic.replace("/In", "")
        #index = self.nodeHandler.findByNameNode(name)
        #if index != -1:
        #self.nodeHandler.nodes[index].lastReceivedMsg = msg.payload.decode()
        '''logMsg = str(msg.topic) + " " + str(msg.payload.decode()) 
        logging.info(logMsg)
        try:
            self.sendToInfluxDB(msg)
        except Exception as e:
            logging.info(str(e))
        '''

    def sendPayload(self, name, payload):
        index = self.nodeHandler.findByNameNode(name)
        pubTopic = self.nodeHandler.nodes[index].pubTopic
        self.nodeHandler.nodes[index].lastSendMsg = payload
        self.client.publish(pubTopic, payload)





def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("#")
    
def on_message(client, userdata, msg):
    userdata.changeData(msg)


if __name__ == "__main__":
    m = MqttHandler("127.0.0.1")
    
    #print("write 'stop' to end")
    #exitCommand = ""
    while(True):
        #exitCommand = input()
        pass
        
    
    print("Slutar While")

# C:\Users\KCHBBH\Desktop\IoTHome