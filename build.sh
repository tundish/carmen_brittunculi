#! /bin/sh -

PROJ=carmen

mkdir -p dist
docker rmi $PROJ_app
docker build -t $PROJ_app:latest
