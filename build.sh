#! /bin/sh -

PROJ=carmen

mkdir -p dist
docker rmi $(PROJ)_app
docker build -t $(PROJ)_app:latest
