#!/bin/bash

cd /workdir

yarn config set registry http://registry:4873
yarn install
