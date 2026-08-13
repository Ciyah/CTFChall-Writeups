#!/bin/bash

docker stop web_nomad_notes && docker rm web_nomad_notes
docker build -t web_nomad_notes . && docker run --name web_nomad_notes -p 3000:3000 web_nomad_notes