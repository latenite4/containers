# Dockerfile runAsUser demo
#
FROM busybox 
MAINTAINER Your name
LABEL description="This image allows k8s runAsUser to execute without crash"
ENTRYPOINT echo "Hello from a container...";whoami; ps aux; touch /data/demo/myfile; ls -l /data/demo;sleep 180



