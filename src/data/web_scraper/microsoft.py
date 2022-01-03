#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 31 02:33:45 2021

@author: erinnsun
"""

import requests
from bs4 import BeautifulSoup

orgs = []
content = requests.get("https://opensource.microsoft.com/api/repos").json()
for i in range(content['totalPages']):
    print(i)
    content = requests.get("https://opensource.microsoft.com/api/repos?page=%d"%(i)).json()
    for repo in content['repos']:
        url = repo['html_url']
        org = url.split('/')[3]
        if(org not in orgs):
            orgs.append(org)
    
