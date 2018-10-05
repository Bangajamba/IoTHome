#include "Mqtt.h"
Mqtt mqtt;

void setup() {
  // put your setup code here, to run once:

  Serial.begin(115200);
  //------Setup------
  //MQTT- INIT and SETUP
  mqtt = Mqtt(
    "SSID",
    "PASSWORD",
    "SERVER_IP_ADDRESS",
    "NODE_TOPIC");
  mqtt.Setup();
}

void loop() {
  // put your main code here, to run repeatedly:

  //------Updates, rf update only needed if recieve msg's------
  mqtt.Update();

  /*
  if(mqtt.lastMessage == "command") //byt till get på lastMessage i framtiden(public -> private)
  {
    //do something with "command" (string)
    Serial.println("Msg from broker");
    mqtt.resetLastMessage();
  }
  */
  
  
  // mqtt.publishMsg("ON from arduino");
}
