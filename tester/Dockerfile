FROM ubuntu:18.04

RUN apt-get update -y
RUN apt-get install curl gnupg2 -y

RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg |  apt-key add -
RUN echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list
RUN apt-get update -y
RUN apt-get -o Dpkg::Options::="--force-overwrite" install yarn -y

RUN apt-get install npm -y

RUN mkdir /workdir

WORKDIR /workdir

COPY ./entrypoint.sh /workdir/entrypoint.sh

ENTRYPOINT [ "/workdir/entrypoint.sh" ]
