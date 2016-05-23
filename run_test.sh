#!/bin/bash

docker pull hello-world
docker tag hello-world localhost:5000/hello-world
docker push localhost:5000/hello-world
