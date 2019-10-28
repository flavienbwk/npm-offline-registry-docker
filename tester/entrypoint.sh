#!/bin/bash

cd /workdir

yarn config set registry http://mirror:4873
yarn install
