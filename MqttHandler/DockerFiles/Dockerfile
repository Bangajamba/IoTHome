FROM ubuntu:16.04
COPY . /home/ubuntu/
RUN apt-get update

# Install Mosquitto
RUN apt-get install -y mosquitto mosquitto-clients

RUN apt-get install -y python3
RUN python3 --version
RUN apt-get -y install python3-pip
RUN pip3 --version
RUN pip3 install paho-mqtt
RUN pip3 install influxdb

RUN chmod +x /home/ubuntu
RUN chmod +x /home/ubuntu/MqttHandler/Main.py

#Bash
RUN chmod +x /home/ubuntu/MqttHandler/DockerFiles/job.sh

EXPOSE 1883 8080
CMD bash /home/ubuntu/MqttHandler/DockerFiles/job.sh