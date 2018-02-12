#!/bin/bash
# Script to build docker image and push to docker cloud repo.
# 
# date: 2/2/18
# name: R. Melton
# command: builddocker.sh <path to Dockerfile> <docker repo>  <image version> <docker username>  
#   example: ./builddocker.sh . image_example 1 awardsolutionsuser

 
function usage { 
str=$'usage: builddocker.sh <path to Dockerfile> <docker repo>  <image version> <docker username> \n\n'
echo "$str" 
}

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


docker build -t $2:$3 $1 
# you may or may not want to run the container locally 
#docker run -it --name mycontainer $2:$3
#docker stop $(docker ps -a -q) ;docker rm $(docker ps -a -q)

docker tag $2:$3 $4/$2:$3
docker images
docker login -u $4 --password-stdin < ./afile.txt
docker push $4/$2
docker logout
# remove local tags
docker rmi $2:$3
docker rmi $4/$2:$3
docker images
#check images versions in this repo

#curl -L https://auth.docker.io/token?service=registry.docker.io&scope=repository:awardsolutionsuser/image_example:pull,push
# to list repos for user: curl -L https://hub.docker.com/v2/repositories/awardsolutionsuser/?page_size=200
# API V2 docs https://docs.docker.com/registry/spec/api/#listing-repositories
echo "the following versions are in your docker repo:"
curl -k https://registry.hub.docker.com/v1/repositories/$4/$2/tags

echo "your image can be accessed as $4/$2:$3"





