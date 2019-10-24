#!/bin/bash

echo -e "ADDUSER"
npm-cli-login -u default -p default -e default@example.com -r http://mirror:4873
echo -e "SETREGISTRY"
npm config set registry http://mirror:4873
echo -e "SCRIPT"
python3.7 /pusher.py
