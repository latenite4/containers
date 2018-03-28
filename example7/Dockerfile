# Dockerfile for passing args to HTTP server container
#
FROM ubuntu 
MAINTAINER  R. Melton
LABEL description="image which returns HTML hostname. used as a demo for loadbalancers"
RUN apt-get update && apt-get install -y python apt-utils python-pip
RUN pip install --upgrade pip
RUN pip install termcolor
EXPOSE 81:81
COPY hello_server.py /
ENTRYPOINT /hello_server.py

