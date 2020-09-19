FROM ubuntu:18.04

RUN apt-get update -y
RUN apt-get install curl gnupg2 python3.7 npm git -y

RUN npm install -g npm@6.14.8
RUN git clone https://github.com/tomgold182/npm-bundle.git
RUN cd npm-bundle && npm install -g

COPY ./entrypoint.sh entrypoint.sh
ENTRYPOINT [ "bash", "entrypoint.sh" ]