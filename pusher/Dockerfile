FROM ubuntu:18.04

RUN apt-get update -y
RUN apt-get install curl gnupg2 -y
RUN apt-get install python3.7 -y
RUN apt-get install npm -y

COPY ./npm-cli-login-0.1.1.tgz /npm-cli-login-0.1.1.tgz
COPY ./npm-6.12.0.tgz /npm-6.12.0.tgz
RUN npm install -g /npm-6.12.0.tgz --production
RUN npm install -g /npm-cli-login-0.1.1.tgz --production

COPY ./entrypoint.sh /entrypoint.sh
ENTRYPOINT [ "/entrypoint.sh" ]