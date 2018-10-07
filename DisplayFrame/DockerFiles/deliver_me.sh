docker build -t iotdisplayframe -f ./DisplayFrame/DockerFiles/DockerFile .
docker tag iotdisplayframe bangajamba/iotdisplayframe 
docker push  bangajamba/iotdisplayframe
