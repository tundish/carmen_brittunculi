#! /bin/sh -

PROJ=carmen
HOST=`hostname`

echo "Starting temporary registry"
docker run -d -p 5000:5000 registry:2

mkdir -p dist

docker rmi ${PROJ}_app
docker build -t ${HOST}:5000/${PROJ}_app:latest .

echo "Docker image: " `docker images -q ${PROJ}_app`
docker push ${HOST}:5000/${PROJ}_app:latest

rkt fetch --insecure-options=image docker://${HOST}:5000/${PROJ}_app:latest

echo "Stopping registry"
docker stop `docker ps | grep registry | cut -d' ' -f1`
