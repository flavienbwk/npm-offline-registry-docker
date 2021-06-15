#!/bin/bash

echo -e "Setting up registry $REGISTRY_ENDPOINT..."
npm config set registry $REGISTRY_ENDPOINT

echo -e "Logging in..."
for run in {1..2}
do
/usr/bin/expect <<EOD
spawn npm adduser
expect {
  "Username:" {send "default\r"; exp_continue}
  "Password:" {send "default\r"; exp_continue}
  "Email: (this IS public)" {send "default@default.fr\r"; exp_continue}
}
EOD
done

echo -e "Pushing packages..."
python3.7 /pusher.py
