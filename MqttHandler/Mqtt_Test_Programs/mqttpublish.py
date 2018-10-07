import paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect("localhost", 1883, 60)
client.publish("Pir/In", "temp,20,hum,46")
client.disconnect()