#!/usr/bin/env/python3.7

import json
import os
from os import path
import glob
import errno

download_path = "/packages"
untar_path = "/untared-packages"
registry_url = "http://mirror:4873"


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


if not path.exists(download_path) or not os.path.isdir(download_path):
    print("Download path '" + download_path +
          "' was not found or is not a directory")
    exit(1)
os.chdir(download_path)

files = glob.glob(download_path + "/*.tgz")
if len(files) <= 0:
    print(download_path + "' does not contain any file")
    exit(0)

for archive in files:
    filename = os.path.basename(archive)[:-4]
    untared_path = untar_path + "/" + filename
    untar_command = "tar -xzf " + archive + " -C " + untared_path
    publish_command = "npm publish --registry " + registry_url
    print("> Processing " + archive + " in " + untared_path)
    mkdir_p(untared_path)
    os.system(untar_command)
    os.chdir(untared_path + "/package")
    os.system(publish_command)
