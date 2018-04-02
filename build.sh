#! /bin/sh -

PROJ=carmen

REG=`sudo systemd-run --slice=machine rkt run --insecure-options=image docker://registry`

mkdir -p dist

docker rmi ${PROJ}_app
docker build -t ${PROJ}_app:latest .

echo "Docker image: " `docker images -q ${PROJ}_app`

rkt fetch --insecure-options=image docker://localhost:5000/${PROJ}_app:latest

echo ${REG} | cut -d: -f2 | xargs sudo systemctl stop
