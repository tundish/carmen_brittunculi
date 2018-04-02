#! /bin/sh -

PROJ=carmen

echo "Starting temporary registry"
REG=`sudo systemd-run --slice=machine rkt run --insecure-options=image docker://registry 2>&1`

mkdir -p dist

docker rmi ${PROJ}_app
docker build -t ${PROJ}_app:latest .

echo "Docker image: " `docker images -q ${PROJ}_app`

rkt fetch --insecure-options=image docker://localhost:5000/${PROJ}_app:latest

echo "Stopping registry"
echo ${REG} | cut -d: -f2 | xargs sudo systemctl stop
