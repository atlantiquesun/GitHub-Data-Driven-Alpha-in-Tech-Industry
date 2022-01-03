#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  2 23:32:21 2022

@author: erinnsun
"""

from selenium import webdriver  
from bs4 import BeautifulSoup
import time
import requests

content = requests.get('https://spotify.github.io/').text
soup = BeautifulSoup(content, 'html.parser')
nodes = soup.findAll('div', {'class': 'col-sm-6 col-lg-3'})

orgs = []
for node in nodes:
    url = node.findAll('a')[0].get('href')
    org = url.split('/')[3]
    if org not in orgs:
        orgs.append(org)

