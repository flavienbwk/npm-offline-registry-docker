#!/bin/bash

echo -e "Setting up registry..."
npm config set registry http://registry:4873

echo -e "Logging in..."
for run in {1..2}
do
/usr/bin/expect <<EOD
spawn npm adduser --registry http://registry:4873
expect {
  "Username:" {send "default\r"; exp_continue}
  "Password:" {send "default\r"; exp_continue}
  "Email: (this IS public)" {send "default@default.fr\r"; exp_continue}
}
EOD
done

echo -e "Pushing packages..."
python3.7 /pusher.py
