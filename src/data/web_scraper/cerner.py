#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 29 18:38:37 2021

@author: erinnsun
"""

import requests
from bs4 import BeautifulSoup

content = requests.get("https://engineering.cerner.com/open-source/").text
soup = BeautifulSoup(content, "html.parser")

nodes = soup.findAll('div', {'class': 'col-sm'})
orgs = []

for n in nodes:
    if(len(n.findAll('a')) == 2): # if it is a normal open source project
        url = n.findAll('a')[0].get('href')
        org = url.split('/')[3]
        if(org not in orgs):
            orgs.append(org)
        