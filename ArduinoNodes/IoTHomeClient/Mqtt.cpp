#include "Mqtt.h"


Mqtt::Mqtt()
{

  
}

Mqtt::Mqtt(char *wifi_ssid, char* wifiPassword, char* mqttServerIpAddress, String topic)
{
  ssid = wifi_ssid;
  password = wifiPassword;
  mqtt_server = mqttServerIpAddress;

  String temp = topic;
  strcpy(clientID, temp.c_str());
  Serial.println(clientID);

  temp = topic;
  temp += "/Out";
  strcpy(subTopic, temp.c_str());
  Serial.println(subTopic);

  temp = topic;
  temp += "/In";
  strcpy(pubTopic, temp.c_str());
  Serial.println(pubTopic);
}
  
void Mqtt::Setup()
{
  
  client = PubSubClient(wifiClient);
  setupWifi();

  client.setServer(mqtt_server, 1883);
  client.setCallback([this] (char* topic, byte* payload, unsigned int length) { this->callback(topic, payload, length); });

  Serial.println("MqttSetupDone");

}

void Mqtt::setupWifi() {

  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  //Serial.println(password);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("#######");
  Serial.print("WiFi connected to ");
  Serial.println(ssid);
  Serial.print("WLAN IP address: ");
  Serial.println(WiFi.localIP());
  Serial.print("ESP8266 MAC address: ");
  Serial.println(WiFi.macAddress());
  Serial.println("#######");
  Serial.println("");
}

void Mqtt::callback(char* topic, byte* payload, unsigned int length) {
  // Conver the incoming byte array to a string
  payload[length] = '\0'; // Null terminator used to terminate the char array
  String message = (char*)payload;

  Serial.print("Message arrived on topic: [");
  Serial.print(topic);
  Serial.print("], ");
  Serial.println(message);

  Serial.println(subTopic);

  lastMessage = message;
  // No Confirmation  
  // client.publish(pubTopic, lastMessage.c_str());
}

void Mqtt::publishMsg(String msg)
{
  client.publish(pubTopic, msg.c_str());
}

void Mqtt::Update()
{
  if (!client.connected()) {
    reconnect();
  }
  
  client.loop();  
}


void Mqtt::reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    //Serial.print("Attempting MQTT connection to MQTT-broker: ");
    //Serial.println(mqtt_server);
    // Attempt to connect
    if (client.connect(clientID)) {
      //Serial.println("");
      //Serial.println("#######");
      Serial.println("SUCCESS connection to MQTT-broker: ");
      Serial.println(mqtt_server);
      // Once connected, publish an announcement...
      //client.publish(pubTopic, "Test publish to broker with QoS = 2 ", 2);
      // ... and resubscribe
      client.subscribe(subTopic);
      //Serial.println("#######");
      //Serial.println("");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

