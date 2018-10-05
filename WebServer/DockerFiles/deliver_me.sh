docker build -t iotwebserver -f ./DockerFiles/DockerFile .
docker tag iotwebserver bangajamba/iotwebserver 
docker push  bangajamba/iotwebserver
