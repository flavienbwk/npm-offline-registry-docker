#!/bin/bash

echo -e "SETREGISTRY"
npm config set registry http://mirror:4873

echo -e "ADDUSER"
/usr/bin/expect <<EOD
spawn npm adduser
expect {
  "Username:" {send "default\r"; exp_continue}
  "Password:" {send "default\r"; exp_continue}
  "Email: (this IS public)" {send "default@default.fr\r"; exp_continue}
}
EOD

echo -e "SCRIPT"
python3.7 /pusher.py
