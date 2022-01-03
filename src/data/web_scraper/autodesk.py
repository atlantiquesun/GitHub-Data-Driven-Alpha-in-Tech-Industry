#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 29 17:45:00 2021

@author: erinnsun
"""

import requests

content = requests.get("https://autodesk.github.io/").text

lines = content.split('\n')

orgs = []
for line in lines:
    if('var orgs =' in line):
        start = line.find('[')
        end = line.find(']')
        line = line[start+1 : end]
        orgs = line.split(',')
        orgs = [x[1:-1] for x in orgs]
        break

