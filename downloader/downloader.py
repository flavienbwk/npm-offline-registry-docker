#!/usr/bin/env/python3.7

import json
import os
from os import path

file_path = "/package.json"
download_path = "/packages"

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
    command = "npm pack " + dependency + "@" + version
    print("> " + command)
    os.system(command)
