#!/usr/bin/env/python3.7

import json
import os
from os import path
import glob
import errno
import time
import requests

START_TIME = time.time()
DOWNLOAD_PATH = "/packages"
UNTAR_PATH = "/untared-packages"
REGISTRY_URL = "http://registry:4873"
PUBLISH_COMMAND = "npm publish --registry " + REGISTRY_URL
PACKAGES_CACHE = True
PACKAGES = {}


def repeat_to_length(string_to_expand, length):
    if (length <= 0):
        return string_to_expand
    return (string_to_expand * length)


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
def generate_cache_from_registry():
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.get(REGISTRY_URL + '/-/verdaccio/packages', headers=headers)
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
    return (package_name in PACKAGES and package_version in PACKAGES[package_name])


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
    if (path.exists(package_directory + "/package.json")):
        if os.path.exists(package_directory + "/node_modules"):
            for module_dir in os.listdir(package_directory + "/node_modules"):
                module_path = package_directory + "/node_modules/" + module_dir
                print(repeat_to_length("\t", recursive + 1) + "> FOUND " + module_dir)
                install_modules(module_path, recursive + 1)
        with open(package_directory + "/package.json", 'r') as file_content:
            content = file_content.read()
        file_content.close()
        if content:
            json_content = json.loads(content)
            if json_content:
                if (set_offline_settings(json_content)):
                    with open(package_directory + "/package.json", 'w') as file_fs:
                        file_fs.write(json.dumps(json_content))
                    file_fs.close()
                # Using the cache system.
                # The program must consider the fact that package directories with 
                # the same name can include different versions.
                if PACKAGES_CACHE:
                    if "name" in json_content and "version" in json_content:
                        if is_package_cached(json_content["name"], json_content["version"]) == False:
                            set_cached_package(json_content["name"], json_content["version"])
                            print(repeat_to_length("\t", recursive) + "> Pushing " + package_directory, flush=True)
                            os.chdir(package_directory)
                            print(package_directory, flush=True)
                            os.system(PUBLISH_COMMAND)
                        else:
                            print(repeat_to_length("\t", recursive) + "> Cached " + package_directory, flush=True)
                    else:
                        print(repeat_to_length("\t", recursive) + "> Invalid settings " + package_directory, flush=True)
                else:
                    os.chdir(package_directory)
                    os.system(PUBLISH_COMMAND)
            else:
                print(repeat_to_length("\t", recursive) + "> Invalid JSON " + package_directory, flush=True)
        else:
            print(repeat_to_length("\t", recursive) + "> Unreadable " + package_directory, flush=True)
    else:
        # Some packages like @babel or @types may be
        # nested in subdirectories.
        for module_dir in os.listdir(package_directory):
            module_path = package_directory + "/" + module_dir
            if (path.exists(module_path + "/package.json")):
                install_modules(module_path, recursive + 1)
    return

if PACKAGES_CACHE:
    cached = generate_cache_from_registry()
    if not cached:
        print("Failed to cache from registry API.")
    else:
        print("Using cache : yes !")

if not path.exists(DOWNLOAD_PATH) or not os.path.isdir(DOWNLOAD_PATH):
    print("Download path '" + DOWNLOAD_PATH +
            "' was not found or is not a directory")
    exit(1)
os.chdir(DOWNLOAD_PATH)

files = glob.glob(DOWNLOAD_PATH + "/*.tgz")
if len(files) <= 0:
    print(DOWNLOAD_PATH + "' does not contain any file")
    exit(0)

for archive in files:
    filename = os.path.basename(archive)[:-4]
    untared_path = UNTAR_PATH + "/" + filename
    untar_command = "tar -xzf " + archive + " -C " + untared_path
    print("> Processing " + archive + " in " + untared_path)
    mkdir_p(untared_path)
    os.system(untar_command)
    os.chdir(untared_path + "/package")
    install_modules(untared_path + "/package", 0)
    
print("\n--- Executed in %s seconds ---" % (time.time() - START_TIME))
