#!/bin/sh

cd $(dirname $0)/..

API_IMAGE_NAME=tomfumb/bvsar-feature-extract-api
docker build \
    -t ${API_IMAGE_NAME} \
    .

# run command needs to mount local src data dir and therefore needs to check for the env var or arg first
