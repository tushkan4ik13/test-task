#!/usr/bin/env bash

set -o allexport
source hello.env
set +o allexport

  if [ $(minikube status | grep Stopped > /dev/null 2>&1; echo $?) -eq 0 ]; then
    echo "Staring minikube.."
    minikube start
  fi

kubectl config set-context minikube

if [ $(helm list | awk '{print $1}' | grep hello-a > /dev/null 2>&1; echo $?) -eq 0 ]; then
  helm upgrade hello-a $HELM_CHART_LOCATION --set app.serviceOwner=customerA
else
  helm install hello-a $HELM_CHART_LOCATION --set app.serviceOwner=customerA
fi

if [ $(helm list | awk '{print $1}' | grep hello-b > /dev/null 2>&1; echo $?) -eq 0 ]; then
  helm upgrade hello-b $HELM_CHART_LOCATION --set app.serviceOwner=customerB
else
  helm install hello-b $HELM_CHART_LOCATION --set app.serviceOwner=customerB
fi