#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  2 19:37:49 2022

@author: erinnsun
"""

import requests
from bs4 import BeautifulSoup
import re

content = requests.get('https://opensource.twitter.dev/projects/').text
soup = BeautifulSoup(content, 'html.parser')

nodes = soup.findAll('div', {'class':'project-card'})

orgs = []
for node in nodes:
    url = node('a', text=re.compile(r'GitHub'))[0].get('href')
    org = url.split('/')[3]
    if(org not in orgs):
        orgs.append(org)