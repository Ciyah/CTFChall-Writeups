#!/bin/bash
docker rm -f web_nextpath
docker build -t web_nextpath .
docker run --name=web_nextpath --rm -p1337:1337 -it web_nextpath
