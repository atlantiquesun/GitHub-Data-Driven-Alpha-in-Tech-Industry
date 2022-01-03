#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  3 00:21:45 2022

@author: erinnsun
"""

import os
import requests

content = requests.get('https://raw.githubusercontent.com/IBM/ibm.github.io/85002f387daa2fadde5974b70629b12a26c8888c/js/orgs.js').text
lines = content.split('\n')

orgs = []
for line in lines:
    if('name' in line):
        full_path = line.split(':')[1]
        if('/' not in full_path): # if it is an organization name
            org = full_path[2:-2]
        else: # ignore repositories
            continue
        if(org not in orgs):
            orgs.append(org)