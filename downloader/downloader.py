#!/usr/bin/env/python3.7

import json
import re
import os
from os import path
import shlex
from subprocess import Popen, PIPE
from threading import Timer

file_path = "/package.json"
download_path = "/packages"

def run_command(cmd, timeout_sec=3600):
    print("Running command : " + cmd)
    proc = Popen(shlex.split(cmd), stdout=PIPE, stderr=PIPE)
    timer = Timer(timeout_sec, proc.kill)
    try:
        timer.start()
        stdout, stderr = proc.communicate()
    finally:
        timer.cancel()
    return (stdout, stderr)

if not path.exists(download_path) or not os.path.isdir(download_path):
    print("Download path '" + download_path + "' was not found or is not a directory")
    exit(1)
os.chdir(download_path)

if not path.exists(file_path):
    print("File package.json '" + file_path + "' was not found")
    exit(1)

with open(file_path, 'r') as file_content:
    content = file_content.read()

if not content:
    print("Content of " + file_path + " is empty or can't be read")
    exit(1)

json_content = json.loads(content)

if not json_content:
    print("Content of " + file_path + " is not a valid JSON")
    exit(1)

if not json_content["dependencies"]:
    print("No dependency found in " + file_path)
    exit(1)

# Use npm-offline-registry
command = f"npo fetch --no-cache --peer -p '{file_path}'"
(stdout, _) = run_command(command)

# Catching `.tar` generated
tars = re.findall(r'packages_[0-9]+\.[0-9]+\.tar', str(stdout))
if not tars and len(tars) == 0:
    print(f"No package tarball found")
    exit(1)

tar = tars[0]
tar_path = f"{download_path}/{tar}"
print(f"Package tarball found : {tar}")

command = f"mv '{tar}' '{tar_path}'"
run_command(command)

print("FINISHED !")
