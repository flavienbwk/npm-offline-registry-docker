#!/usr/bin/env/python3.7

import os
from os import path
import glob
import time
import shlex
from subprocess import Popen, PIPE
from threading import Timer

START_TIME = time.time()
DOWNLOAD_PATH = "/packages"


def run_command(cmd, timeout_sec=3600):
    print("Running command : " + cmd)
    proc = Popen(shlex.split(cmd), stdout=PIPE, stderr=PIPE)
    timer = Timer(timeout_sec, proc.kill)
    try:
        timer.start()
        stdout, stderr = proc.communicate()
        print(stdout, stderr, flush=True)
    finally:
        timer.cancel()
    return (stdout, stderr)


if not path.exists(DOWNLOAD_PATH) or not os.path.isdir(DOWNLOAD_PATH):
    print("Download path '" + DOWNLOAD_PATH + "' was not found or is not a directory")
    exit(1)
os.chdir(DOWNLOAD_PATH)

files = glob.glob(DOWNLOAD_PATH + "/*.tar")
if len(files) <= 0:
    print(DOWNLOAD_PATH + "' does not contain any file")
    exit(0)

for archive in files:
    (stdout, stderr) = run_command(f"npo publish -s '{archive}'")

print("\n--- Executed in %s seconds ---" % (time.time() - START_TIME))
