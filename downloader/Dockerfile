FROM ubuntu:18.04

RUN apt-get update -y
RUN apt-get install curl gnupg2 -y
RUN apt-get install python3.7 -y
RUN apt-get install npm -y

COPY ./entrypoint.sh /entrypoint.sh
ENTRYPOINT [ "/entrypoint.sh" ]