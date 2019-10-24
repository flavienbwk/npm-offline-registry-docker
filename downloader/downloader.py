#!/usr/bin/env/python3.7

import json
import os
from os import path
import shlex
from subprocess import Popen, PIPE
from threading import Timer

file_path = "/package.json"
download_path = "/packages"

def run_command(cmd, timeout_sec):
    proc = Popen(shlex.split(cmd), stdout=PIPE, stderr=PIPE)
    timer = Timer(timeout_sec, proc.kill)
    try:
        timer.start()
        stdout, stderr = proc.communicate()
    finally:
        timer.cancel()

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

dependencies = json_content["dependencies"]
for dependency, version in dependencies.items():
    dep_version = dependency + "@" + version
    command = "npm-bundle " + dep_version
    print("> " + dep_version)
    run_command(command, 120)
