import paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect("localhost", 1883, 60)
client.publish("Pir/In", 'temp,6,hum,30.4')
client.disconnect()