#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  1 16:53:17 2022

@author: erinnsun
"""


from selenium import webdriver  
from bs4 import BeautifulSoup
import time

driver_path = "/Users/erinnsun/Desktop/web_scraper/chromedriver"
driver = webdriver.Chrome(driver_path)

url = "https://epam.github.io/"
driver.get(url)
time.sleep(5)

content = driver.page_source
soup = BeautifulSoup(content, 'html.parser')
nodes = soup.findAll('epamghio-project-item')

orgs = []
for node in nodes:
    url = node.findAll('a', {'class':'name'})[0].get('href')
    org = url.split('/')[3]
    if(org not in orgs):
        orgs.append(org)