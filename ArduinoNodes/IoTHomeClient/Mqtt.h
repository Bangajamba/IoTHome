#ifndef MQTT_H
#define MQTT_H

#include <ESP8266WiFi.h>
#include <PubSubClient.h>

class Mqtt{
  
  public:
        Mqtt();
        Mqtt(char* ssid, char* wifiPassword, char* mqttServerIpAddres, String topic);
        // TODO: Constructor with wifi and nodename
        void Setup();
        void Update();
        String lastMessage;
        void resetLastMessage() {lastMessage = "";}
        void publishMsg(String msg);
  private:

        char* ssid = "";
        char* password = "";
        char* mqtt_server = ""; //MqttServer
        char* clientID = "";
        char* pubTopic = ""; //(In)
        char* subTopic = "";//(Out)
        WiFiClient wifiClient;
        PubSubClient client;
        char msg[50];
        void setupWifi();
        void callback(char* topic, byte* payload, unsigned int length);
        void reconnect();
};

#endif
