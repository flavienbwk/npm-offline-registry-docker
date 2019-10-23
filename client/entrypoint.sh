#!/bin/bash

cd /workdir

yarn config set registry "http://mirror:80/"
yarn install

yarn add mime-types-2.1.24