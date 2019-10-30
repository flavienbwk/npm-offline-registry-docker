FROM ubuntu:18.04

RUN apt-get update -y
RUN apt-get install curl gnupg2 -y
RUN apt-get install python3.7 python3-pip -y
RUN apt-get install npm -y

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get install expect -y

COPY ./npm-6.12.0.tgz /npm-6.12.0.tgz
COPY ./npm-bundle-3.0.3.tgz /npm-bundle-3.0.3.tgz
RUN npm install -g /npm-6.12.0.tgz --production
RUN npm install -g /npm-bundle-3.0.3.tgz --production

RUN python3.7 -m pip install --upgrade pip
RUN pip install requests

COPY ./entrypoint.sh /entrypoint.sh
ENTRYPOINT [ "/entrypoint.sh" ]