#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  3 01:04:04 2022

@author: erinnsun
"""



from selenium import webdriver  
from bs4 import BeautifulSoup
import time

driver_path = "/Users/erinnsun/Desktop/web_scraper/chromedriver"
driver = webdriver.Chrome(driver_path)

url = "https://uber.github.io/#/github"
driver.get(url)
time.sleep(10)

content = driver.page_source
soup = BeautifulSoup(content, 'html.parser')
nodes = soup.findAll('a', {'data-baseweb':'button'})

orgs = []
for node in nodes:
    if(node.text == 'View on GitHub'):
        url = node.get('href')
        org = url.split('/')[3]
        if org not in orgs:
            orgs.append(org)
            