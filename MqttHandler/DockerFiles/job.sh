#!/bin/sh
echo "startjob"
/etc/init.d/mosquitto start #
# mosquitto #added comment fix \r problem
python3 /home/ubuntu/MqttHandler/Main.py 172.18.0.1 #
echo "started mosquitto"