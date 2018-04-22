# Dockerfile for passing args to HTTP server container
#
FROM golang:latest 
MAINTAINER  R. Melton
LABEL description="image which returns HTML hostname. used as a demo for loadbalancers"
#RUN apt-get update && apt-get install -y python apt-utils python-pip
#RUN pip install --upgrade pip
#RUN pip install termcolor
EXPOSE 82:82
COPY hello-server /
ENTRYPOINT /hello-server

