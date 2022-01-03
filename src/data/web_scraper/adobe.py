#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  1 15:44:20 2022

@author: erinnsun
"""


from selenium import webdriver  
from bs4 import BeautifulSoup
import time

driver_path = "/Users/erinnsun/Desktop/web_scraper/chromedriver"
driver = webdriver.Chrome(driver_path)

url = "https://opensource.adobe.com//"
driver.get(url)
time.sleep(5)

content = driver.page_source
soup = BeautifulSoup(content, 'html.parser')
nodes = soup.findAll('a', {'org':'actOrg'})

orgs = []
for node in nodes:
    url = node.get('href')
    org = url.split('/')[3]
    if(org not in orgs):
        orgs.append(org)
