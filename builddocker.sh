#!/bin/bash
# Script to build docker image and push to docker cloud repo.
# 
# date: 2/2/18
# name: R. Melton
# command: builddocker.sh <path to Dockerfile> <docker username>  <docker repo> <image version>  
#   example: ./builddocker.sh . awardsolutionsuser image_example 1 

 
function usage { 
  str=$'usage: builddocker.sh <path to Dockerfile> <docker username>  <docker repo name> <image version> \n\n'
  echo "$str"
  echo 
}

if [ "$#" -ne 4 ];then
  echo "invalid paramater list"
  usage
  exit 1
fi

if [ -e "$1/Dockerfile" ]
then
  echo "Dockerfile found."
else
  echo "Dockerfile not found."
  usage
  exit 1
fi
if [ ! -e "./afile.txt" ]
then
  echo "missing local afile.txt in " `pwd`
  exit 1
fi
LOCALDOCKERCONFIG=~/.docker/config.json

docker build -t $3:$4 $1 
# you may or may not want to run the container locally 
#docker run -it --name mycontainer $2:$3
#docker stop $(docker ps -a -q) ;docker rm $(docker ps -a -q)

docker tag $3:$4 $2/$3:$4
docker images
docker login -u $2 --password-stdin < ./afile.txt
grep "index.docker.io" $LOCALDOCKERCONFIG
if [ ! "$?" -eq 0 ]; then
  echo "docker repo login error; cannot continue"
  exit 1
fi
docker push $2/$3
docker logout
# remove local tags
docker rmi $3:$4
docker rmi $2/$3:$4
docker images
#check images versions in this repo

#curl -L https://auth.docker.io/token?service=registry.docker.io&scope=repository:awardsolutionsuser/image_example:pull,push
# to list repos for user: curl -L https://hub.docker.com/v2/repositories/awardsolutionsuser/?page_size=200
# API V2 docs https://docs.docker.com/registry/spec/api/#listing-repositories
echo "the following versions are in your docker repo:"
curl -k https://registry.hub.docker.com/v1/repositories/$2/$3/tags
echo
echo "your image can be accessed as $2/$3:$4"
echo





