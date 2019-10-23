FROM ubuntu:18.04

RUN apt-get update -y
RUN apt-get install curl gnupg2 apache2 -y

RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg |  apt-key add -
RUN echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list
RUN apt-get update -y
RUN apt-get -o Dpkg::Options::="--force-overwrite" install yarn -y

# YARN CONFIGURATION
# Thank you https://yarnpkg.com/blog/2016/11/24/offline-mirror/
RUN mkdir -p /var/www/mirror/packages

WORKDIR /var/www/mirror
COPY ./mirror/package.json /var/www/mirror/package.json

RUN yarn install
RUN yarn config set yarn-offline-mirror /var/www/mirror/packages
RUN yarn config set yarn-offline-mirror-pruning true
RUN rm -rf node_modules/ yarn.lock
RUN yarn install

RUN yarn cache clean
RUN yarn install --offline

# WEBSERVER CONFIGURATION
COPY ./apache2.conf /etc/apache2/sites-available/000-default.conf
COPY ./entrypoint.sh /entrypoint.sh

ENTRYPOINT [ "/entrypoint.sh" ]
EXPOSE 80