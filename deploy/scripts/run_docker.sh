#!/usr/bin/env bash

set -o allexport
source hello.env
set +o allexport

docker run -d -p $SERVER_PORT:$SERVER_PORT \
    -e "SERVICE_OWNER=customerB" \
    -e "SERVER_PORT=$SERVER_PORT" \
    $IMAGE_NAME:$IMAGE_VERSION
  
if [ $? -eq 0 ]; then
  echo "Hello API service was started locally. Please check http://localhost:$SERVER_PORT"
else
  echo "Unable to start Hello API service in Docker"
fi
