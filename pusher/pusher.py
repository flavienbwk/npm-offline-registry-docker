#!/usr/bin/env/python3.7

import os
from os import path
import glob
import time
import shlex
from subprocess import Popen, PIPE

START_TIME = time.time()
DOWNLOAD_PATH = "/packages"
UNTAR_PATH = "/untared-packages"
REGISTRY_URL = os.environ.get("REGISTRY_ENDPOINT")


def run_command(cmd):
    print("Running command : " + cmd, flush=True)
    proc = Popen(shlex.split(cmd), stdout=PIPE, stderr=PIPE, universal_newlines=True)
    for stdout_line in iter(proc.stdout.readline, ""):
        yield stdout_line
    proc.stdout.close()
    return_code = proc.wait()
    return return_code


if not path.exists(DOWNLOAD_PATH) or not os.path.isdir(DOWNLOAD_PATH):
    print("Download path '" + DOWNLOAD_PATH + "' was not found or is not a directory")
    exit(1)
os.chdir(DOWNLOAD_PATH)

files = glob.glob(DOWNLOAD_PATH + "/*.tar")
if len(files) <= 0:
    print(DOWNLOAD_PATH + "' does not contain any file")
    exit(0)

for archive in files:
    for line in run_command(f"npo publish -s '{archive}'"):
        print(line, end="", flush=True)

print("\n--- Executed in %s seconds ---" % (time.time() - START_TIME))
