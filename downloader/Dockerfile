FROM ubuntu:18.04

RUN apt-get update -y
RUN apt-get install curl gnupg2 -y
RUN apt-get install python3.7 -y
RUN apt-get install npm -y

RUN npm install -g npm@6.12.0
RUN npm install -g npm-bundle

COPY ./entrypoint.sh /entrypoint.sh
ENTRYPOINT [ "/entrypoint.sh" ]