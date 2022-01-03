#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 29 19:01:38 2021

@author: erinnsun
"""

import requests
from bs4 import BeautifulSoup 

content = requests.get("https://www.twilio.com/open-source").text
soup = BeautifulSoup(content, 'html.parser')
nodes = soup.findAll('a', {'class': 'btn btn--secondary'})

nodes2 = soup.findAll('ul', {'class': 'docs-article__list'})[0].findAll('a')
nodes.extend(nodes2)

orgs = []
for node in nodes:
    url = node.get('href')
    if('github.com' in url):
        org = url.split('/')[3]
        if(org not in orgs):
            orgs.append(org)



    


