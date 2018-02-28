# Dockerfile runAsUser demo
#
FROM ubuntu 
MAINTAINER Your name
LABEL description="This image allows k8s runAsUser to execute without crash"
RUN apt-get update && apt-get install -y python apt-utils
COPY read_secrets.py /
ENV FROMDOCKERFILE1=FROMDOCKERFILEVALUE1 FROMDOCKERFILE2=FROMDOCKERFILEVALUE2
ENTRYPOINT echo "Hello from a container...";date ; env;echo "data key:values form cm2; cat /etc/depl/config/deplconfig.yml; echo  ; ls -la /etc/secrets; echo ; echo "dump secrets ";  /read_secrets.py; sleep 120

 
