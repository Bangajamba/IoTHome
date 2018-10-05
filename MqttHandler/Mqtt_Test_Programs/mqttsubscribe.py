import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("#")
    
def on_message(client, userdata, msg):
    print(msg.topic)
    print(msg.payload.decode())

listenClient = mqtt.Client()
listenClient.on_connect = on_connect
listenClient.on_message = on_message
listenClient.connect("localhost", 1883, 60)

listenClient.loop_forever()