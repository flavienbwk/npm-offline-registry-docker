#!/bin/bash

cd /workdir

yarn config set registry http://localhost:4873

yarn install
yarn add mime-types

cat package.json