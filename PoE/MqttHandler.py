from threading import Thread
import paho.mqtt.client as mqtt
import logging

class MqttHandler():

    def __init__(self, ip, broker):
        self.mqttConnected = False #not in use
        self.ip = ip
        self.connectMqtt(broker)

    def connectMqtt(self, broker):
        try:
            # MqttListener used for receive incoming message(subscribe)
            self.listenClient = mqtt.Client(userdata=broker)
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


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("#")
    
def on_message(client, userdata, msg):
    userdata.on_message(msg)