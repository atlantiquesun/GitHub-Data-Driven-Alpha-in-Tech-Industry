#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 31 01:43:27 2021

@author: erinnsun
"""

import re
import requests
from bs4 import BeautifulSoup

def get_org(git_url):
    
    full = git_url.split('/')[3]
    return full.split('?')[0] # discard the repository name


content = requests.get("https://opensource.apple.com/projects/").text
soup = BeautifulSoup(content, 'html.parser')

apple_projects = soup.findAll('section', {'class': 'section section-apple bg-gray'})[0]
buttons = apple_projects.findAll('a', {'class': 'button button-neutral button-reduced'})

urls = []
for b in buttons:
    if(b.find(text=re.compile("Details"))):
        url = b.get('href')
        if(url not in urls):
            urls.append(url)

url_root = 'https://opensource.apple.com'
urls = [url_root + x for x in urls]

orgs = []
apache_buttons = []
for url in urls:
    content = requests.get(url).text
    soup = BeautifulSoup(content, 'html.parser')
    buttons = soup.findAll('a', {'class': 'button button-neutral button-reduced'})
    
    for b in buttons:
        if(b.find(text=re.compile("GitHub"))):
            org = get_org(b.get('href'))
            if(org not in orgs):
                orgs.append(org)
            if(org == 'apache'):
                apache_buttons.append(b)
                
            

    