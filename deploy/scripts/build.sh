#!/usr/bin/env bash

set -o allexport
source hello.env
set +o allexport

pushd $SOURCE_LOCATION
yq -i ".info.version = env(IMAGE_VERSION)" source/modules/api/hello/swagger.yml
docker build --tag $IMAGE_NAME:$IMAGE_VERSION \
    --target hello_api . \
    && echo "Docker image $IMAGE_NAME:$IMAGE_VERSION was created"

if [ $PUSH_TO_MINIKUBE == "true" ]; then
  if [ $(minikube status | grep Stopped > /dev/null 2>&1; echo $?) -eq 0 ]; then
    echo "Staring minikube.."
    minikube start
  fi
  echo "Adding $IMAGE_NAME:$IMAGE_VERSION to minikube"
  minikube image load $IMAGE_NAME:$IMAGE_VERSION
fi
popd

echo "Updating Hello API Helm chart"
yq -i ".image.tag = env(IMAGE_VERSION)" $HELM_CHART_LOCATION/values.yaml
yq -i ".appVersion = env(IMAGE_VERSION)" $HELM_CHART_LOCATION/Chart.yaml

echo "Done!"
