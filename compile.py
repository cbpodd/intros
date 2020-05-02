#!/usr/bin/env python3

import sys
import json
import os
from pathlib import Path

WINDOWS = 'windows'
LINUX = 'linux'
MACOS = 'macos'
UNIX = 'unix'
FILES_DIR = 'files'
CONFIG_DIR = 'config'
HOME = str(Path.home())
CWD = os.getcwd()

def main():
    with open('intros.json') as f:
        data = json.load(f)
        os_type = sys.platform
        platform_name = ''
        fs_type = UNIX
        if os_type.startswith('darwin'):
            platform_name = MACOS
        elif os_type.startswith('win32'):
            platform_name = WINDOWS
        elif os_type.startswith('linux'):
            platform_name = LINUX

        if platform_name == WINDOWS:
            fs_type = WINDOWS

        files = data['files']['shared'] + data['files'][platform_name]
        folders = data['folders']['shared'] + data['folders'][platform_name]
        config = data['config']['shared'] + data['config'][platform_name]

        if fs_type == UNIX:
            return unix(files, folders, config)

        return windows(files, folders, config)

def unix(files, folders, config):
    hiddenConfig = hidden(CONFIG_DIR, UNIX)
    for f in files:
        fullPath = os.path.join(CWD, FILES_DIR, f)
        hf = hidden(f, UNIX)
        homePath = os.path.join(HOME, hf)
        if os.path.isfile(fullPath) and not os.path.isfile(homePath):
            os.symlink(fullPath, homePath)
    for folder in folders:
        fullPath = os.path.join(CWD, folder)
        hf = hidden(folder, UNIX)
        homePath = os.path.join(HOME, hf)
        if os.path.isdir(fullPath) and not os.path.isdir(homePath):
            os.symlink(fullPath, homePath)
    configPath = os.path.join(HOME, hiddenConfig)
    if not os.path.isdir(configPath):
        os.makedirs(configPath)
    for c in config:
        fullPath = os.path.join(CWD, CONFIG_DIR, c)
        homePath = os.path.join(configPath, c)
        if os.path.exists(fullPath) and not os.path.exists(homePath):
            os.symlink(fullPath, homePath)
    return 0

def windows(files, folders, config):
    return 1

def hidden(f, fs_type):
    if fs_type == UNIX:
        return "." + f

    return "_" + f

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
