#!/bin/bash
docker rm -f web-ssos
docker build -t web-ssos .
docker run -p 12345:1337 --name web-ssos web-ssos