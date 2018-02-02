# Dockerfile runAsUser demo
#
FROM busybox 
MAINTAINER Your name
LABEL description="This image allows k8s runAsUser to execute without crash"
ENTRYPOINT echo "Hello from a container...";sleep 10



