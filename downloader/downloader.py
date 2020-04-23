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

dependencies = json_content["dependencies"]
for dependency, version in dependencies.items():
    dep_version = dependency + "@" + version
    command = "npm-bundle " + dep_version + " -f"
    print("> " + dep_version)

    npm_bundle_success = False
    print("     > Trying to npm-bundle")
    (stdout, stderr) = run_command(command, 3600)
    if len(str(stderr)) == 0:
        print("OUT: " + str(stdout))
        npm_bundle_success = True
    else:
        print("ERR: " + str(stderr))

    if npm_bundle_success is False:
        # Depth 1 module failover
        dep_version_equal = dependency + "==" + version
        print("     > Trying to npm-bundle manually")
        command = "npm install " + dep_version_equal
        (stdout, stderr) = run_command(command, 3600)
        if len(str(stderr)) == 0:
            print("OUT: " + str(stdout))
            module_path = "{}/node_modules/{}".format(download_path, dependency)
            if os.path.exists(module_path):
                os.chdir(module_path)
                run_command("npm install", 3600)
                os.chdir(download_path)
                run_command("tar cvzf {}.tgz {}".format(dependency, module_path), 3600)
            else:
                # TODO(flavienbwk) : Add git clone + npm install functionality to pack the module
                print("     > {} does not exist".format(module_path))
        else:
            print("ERR: " + str(stderr))
