docker build -t iothome -f ./MqttHandler/DockerFiles/DockerFile .
docker tag iothome bangajamba/iothome 
docker push  bangajamba/iothome
