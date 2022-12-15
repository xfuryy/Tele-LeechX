#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) 5MysterySD | Anasty17 ( MLTB ) | HuzunluArtemis
#
# Copyright 2022 - TeamTele-LeechX
# 
# This is Part of < https://github.com/5MysterySD/Tele-LeechX >
# All Right Reserved
import pkg_resources
from logging import FileHandler, StreamHandler, INFO, basicConfig, error as log_error, info as log_info
from os import path as ospath, environ, listdir
from subprocess import run as srun, call as scall
from requests import get as rget
from dotenv import load_dotenv
 
searchLogFile = listdir()
for log in searchLogFile:
    if log.endswith('Logs.txt'):
        with open(log, 'r+') as f:
              f.truncate(0)

basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[FileHandler('Logs.txt'), StreamHandler()],
                    level=INFO)

CONFIG_FILE_URL = environ.get('CONFIG_FILE_URL')
try:
    if len(CONFIG_FILE_URL) == 0:
        raise TypeError
    try:
        res = rget(CONFIG_FILE_URL)
        if res.status_code == 200:
            with open('config.env', 'wb+') as f:
                f.write(res.content)
        else:
            log_error(f"Failed to download config.env {res.status_code}")
    except Exception as e:
        log_error(f"CONFIG_FILE_URL: {e}")
except:
    pass

load_dotenv('config.env', override=True)

## Update Packages ++++
if environ.get('UPDATE_EVERYTHING_WHEN_RESTART', 'False').lower() == 'true':
    packages = [dist.project_name for dist in pkg_resources.working_set]
    scall("pip install --upgrade " + ' '.join(packages), shell=True)
## Update Packages ----

UPSTREAM_REPO = environ.get('UPSTREAM_REPO', "https://github.com/5MysterySD/Tele-LeechX")
UPSTREAM_BRANCH = environ.get('UPSTREAM_BRANCH', "h-code")
try:
    if len(UPSTREAM_REPO) == 0:
       raise TypeError
except:
    UPSTREAM_REPO = None
try:
    if len(UPSTREAM_BRANCH) == 0:
       raise TypeError
except:
    UPSTREAM_BRANCH = 'h-code' #Never Put Heroku Here !!

if UPSTREAM_REPO is not None:
    if ospath.exists('.git'):
        srun(["rm", "-rf", ".git"])
        
    update = srun([f"git init -q \
                     && git config --global user.email mysterysd.sd@gmail.com \
                     && git config --global user.name tele-leechx \
                     && git add . \
                     && git commit -sm update -q \
                     && git remote add origin {UPSTREAM_REPO} \
                     && git fetch origin -q \
                     && git reset --hard origin/{UPSTREAM_BRANCH} -q"], shell=True)

    if update.returncode == 0:
        log_info(f'Successfully updated with latest commit from {UPSTREAM_REPO}')
    else:
        log_error(f'Something went wrong while updating, check {UPSTREAM_REPO} if valid or not!')
