FROM ubuntu:latest
LABEL authors="adefo"

ENTRYPOINT ["top", "-b"]