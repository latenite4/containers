# Dockerfile for passing args to container
#
FROM ubuntu 
MAINTAINER  R. Melton
LABEL description="This image allows user to pass args to container when it starts"
RUN apt-get update && apt-get install -y python apt-utils
COPY read-args1.py /
ENV FROMDOCKERFILE1=FROMDOCKERFILEVALUE1
ENTRYPOINT /read-args1.py ; env;sleep 120

