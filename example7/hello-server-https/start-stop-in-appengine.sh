#!/bin/bash
# start-stop-in-appengine.sh - a program to start an app on GCP appengine or stop it
#
# command: start-stop-in-appengine.sh [init version | delete]
# date: 5/15/19
# name: R. Melton


function usage {
  echo "error: invalid parameters; must be"
  echo "  start-stop-in-appengine.sh [init version | delete ] "
  exit 1
}


if [ $# -lt 1 ]
then
  usage
fi;
if [ "$1" != "init" ] && [ "$1" != "delete" ] ; then
  usage
fi

#create
# create or delete the k8s cluster on GCP
if [ "$1" = "init" ]; then
  APP_VER=$2
  gcloud app deploy --project=$MY_GCP_PROJECT  --version=$APP_VER -q

  echo "target URL for service is: https://\$MY_GCP_PROJECT.appspot.com"

#delete
elif [ "$1" = "delete" ]; then
  APP_VER=`gcloud app instances list  --format json | jq --raw-output '.[0].version'`
  echo "deleting appengine version: $APP_VER"
  gcloud app versions stop -q $APP_VER
  gcloud app instances list
fi
