docker build -t iotwebserver -f ./WebServer/DockerFiles/DockerFile .
docker tag iotwebserver bangajamba/iotwebserver 
docker push  bangajamba/iotwebserver
