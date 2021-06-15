FROM ubuntu:18.04

RUN apt-get update && apt-get install curl gnupg2 python3.7 python3-pip npm -y

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get install expect -y

RUN python3.7 -m pip install --upgrade pip
RUN pip install requests

COPY ./npm-6.14.8.tgz /npm-6.14.8.tgz
RUN npm install -g /npm-6.14.8.tgz --production
RUN npm install -g npm-offline-packager@1.3.0

COPY ./entrypoint.sh /entrypoint.sh
ENTRYPOINT [ "/entrypoint.sh" ]