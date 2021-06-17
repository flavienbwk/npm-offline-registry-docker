#!/usr/bin/env/python3.7

import os
from os import path
import glob
import time
import errno
import requests
import shlex
import json
from subprocess import Popen, PIPE

START_TIME = time.time()
DOWNLOAD_PATH = "/packages"
UNTAR_PATH = "/untared-packages"
REGISTRY_URL = os.environ.get("REGISTRY_ENDPOINT")
PUBLISH_COMMAND = "npm publish --registry " + REGISTRY_URL
PACKAGES_CACHE = True
PACKAGES = {}


def repeat_to_length(string_to_expand, length):
    if length <= 0:
        return string_to_expand
    return string_to_expand * length


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


# Will parse the Verdaccio's API to find
# already pushed packages.
def generate_cache_from_mirror():
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.get(f"{REGISTRY_URL}/-/verdaccio/packages", headers=headers)
        packages = response.json()
        if packages:
            for package in packages:
                if "name" in package and "version" in package:
                    set_cached_package(package["name"], package["version"])
        else:
            return False
    except Exception as ex:
        print(ex)
        return False
    return True


# Returns True if the package is already installed
# and False if it is not.
def set_cached_package(package_name, package_version):
    if package_name in PACKAGES:
        if package_version not in PACKAGES[package_name]:
            PACKAGES[package_name].append(package_version)
    else:
        PACKAGES[package_name] = [package_version]


def is_package_cached(package_name, package_version):
    return package_name in PACKAGES and package_version in PACKAGES[package_name]


# Handling the fact a registry can be hard-coded in
# the 'publishConfig' option : removing it
# OR
# that 'scripts._prepublish' might be defined, running
# scripts with dev-dependencies, not downloaded by
# npm-bundle.
def set_offline_settings(json_content):
    modified = False
    if "scripts" in json_content and "_prepublish" in json_content["scripts"]:
        modified = True
        json_content["scripts"].pop("_prepublish", None)
    if "publishConfig" in json_content and "registry" in json_content["publishConfig"]:
        modified = True
        json_content["publishConfig"].pop("registry", None)
    return modified


def install_modules(package_directory, recursive=0):
    if path.exists(package_directory + "/package.json"):
        if os.path.exists(package_directory + "/node_modules"):
            for module_dir in os.listdir(package_directory + "/node_modules"):
                module_path = package_directory + "/node_modules/" + module_dir
                print(repeat_to_length("\t", recursive + 1) + "> FOUND " + module_dir)
                install_modules(module_path, recursive + 1)
        with open(package_directory + "/package.json", "r") as file_content:
            content = file_content.read()
        file_content.close()
        if content:
            json_content = json.loads(content)
            if json_content:
                if set_offline_settings(json_content):
                    with open(package_directory + "/package.json", "w") as file_fs:
                        file_fs.write(json.dumps(json_content))
                    file_fs.close()
                # Using the cache system
                # Must consider the fact package directories with same name
                # can include different versions.
                if PACKAGES_CACHE:
                    if "name" in json_content and "version" in json_content:
                        if (
                            is_package_cached(
                                json_content["name"], json_content["version"]
                            )
                            == False
                        ):
                            set_cached_package(
                                json_content["name"], json_content["version"]
                            )
                            print(
                                repeat_to_length("\t", recursive)
                                + "> Pushing "
                                + package_directory
                            )
                            os.chdir(package_directory)
                            print(f"> {PUBLISH_COMMAND}", flush=True)
                            os.system(PUBLISH_COMMAND)
                        else:
                            print(
                                repeat_to_length("\t", recursive)
                                + "> Cached "
                                + package_directory
                            )
                    else:
                        print(
                            repeat_to_length("\t", recursive)
                            + "> Invalid settings "
                            + package_directory
                        )
                else:
                    os.chdir(package_directory)
                    print(f"> {PUBLISH_COMMAND}", flush=True)
                    os.system(PUBLISH_COMMAND)
            else:
                print(
                    repeat_to_length("\t", recursive)
                    + "> Invalid JSON "
                    + package_directory
                )
        else:
            print(
                repeat_to_length("\t", recursive) + "> Unreadable " + package_directory
            )
    else:
        # Some packages like @babel or @types may be
        # nested in subdirectories.
        for module_dir in os.listdir(package_directory):
            module_path = package_directory + "/" + module_dir
            if path.exists(module_path + "/package.json"):
                install_modules(module_path, recursive + 1)
    return


def run_command(cmd):
    print("Running command : " + cmd, flush=True)
    proc = Popen(shlex.split(cmd), stdout=PIPE, stderr=PIPE, universal_newlines=True)
    for stdout_line in iter(proc.stdout.readline, ""):
        print(stdout_line, flush=True)
    proc.stdout.close()
    return_code = proc.wait()
    return return_code


if PACKAGES_CACHE:
    cached = generate_cache_from_mirror()
    if not cached:
        print("Failed to cache from mirror API.")
    else:
        print("Using cache : yes !")

if not path.exists(DOWNLOAD_PATH) or not os.path.isdir(DOWNLOAD_PATH):
    print("Download path '" + DOWNLOAD_PATH + "' was not found or is not a directory")
    exit(1)
os.chdir(DOWNLOAD_PATH)

if not path.exists(DOWNLOAD_PATH) or not os.path.isdir(DOWNLOAD_PATH):
    print("Download path '" + DOWNLOAD_PATH + "' was not found or is not a directory")
    exit(1)
os.chdir(DOWNLOAD_PATH)

tar_files = glob.glob(DOWNLOAD_PATH + "/*.tar")
if len(tar_files) <= 0:
    print(DOWNLOAD_PATH + "' does not contain any file")
    exit(0)

for tar_file in tar_files:

    # 1. Extract TGZs
    tar_basename = os.path.basename(tar_file)[:-4]
    untared_path = f"{UNTAR_PATH}/{tar_basename}"
    untar_command = f"tar -xvf '{tar_file}' -C '{UNTAR_PATH}'"
    mkdir_p(untared_path)
    os.system(untar_command)

    # 2. NPM publish each TGZ
    os.chdir(untared_path)
    tgz_files = glob.glob(f"{untared_path}/*.tgz")
    if len(tgz_files) <= 0:
        print(untared_path + "' does not contain any TGZ file. Skipping...")
        continue
    for tgz_file in tgz_files:
        tgz_basename = os.path.basename(tgz_file)[:-4]
        untgz_path = f"{untared_path}/{tgz_basename}"
        untgz_command = f"tar -xzf '{tgz_file}' -C '{untgz_path}'"
        print(f"> Processing {tgz_file} in {untgz_path} from {tar_basename}")
        mkdir_p(untgz_path)
        os.system(untgz_command)
        # Get first directory inside untgzed TGZ
        subdirs = os.listdir(untgz_path)
        if not subdirs:
            print(f"> WARN: No subdir in package, trying to find package.json")
            if not os.path.exists(f"{untgz_path}/package.json"):
                print(f"> ERR: INCOMPATIBLE FORMAT FOR PACKAGE, skipping...")
                continue
        else:
            untgz_path = f"{untgz_path}/{subdirs[0]}"
        os.chdir(untgz_path)
        install_modules(untgz_path, 0)


print("\n--- Executed in %s seconds ---" % (time.time() - START_TIME))
