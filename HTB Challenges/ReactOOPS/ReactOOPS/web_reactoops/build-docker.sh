#!/bin/bash
NAME="reactoops"
docker rm -f web_$NAME
docker build --tag=web_$NAME .
if [ -z "$1" ]; then
    DEBUG="--detach"
elif [[ "$1" == "debug" ]]; then
    DEBUG=""
fi
docker run -p 1337:1337 --rm --name=web_$NAME $DEBUG web_$NAME
