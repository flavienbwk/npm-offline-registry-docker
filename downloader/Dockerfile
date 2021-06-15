FROM ubuntu:18.04

RUN apt-get update && apt-get install curl gnupg2 python3.7 npm git -y

ENV DEBIAN_FRONTEND noninteractive
RUN npm install -g npm@6.14.8
RUN npm install -g npm-offline-packager@1.3.0

COPY ./entrypoint.sh entrypoint.sh
ENTRYPOINT [ "bash", "entrypoint.sh" ]