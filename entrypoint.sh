#!/bin/bash

chown -R www-data:root /var/www/mirror
/usr/sbin/apache2ctl -D FOREGROUND