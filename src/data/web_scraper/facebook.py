#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  2 18:53:51 2022

@author: erinnsun
"""

from selenium import webdriver  
from bs4 import BeautifulSoup
import time

driver_path = "/Users/erinnsun/Desktop/web_scraper/chromedriver"
driver = webdriver.Chrome(driver_path)

url = "https://opensource.fb.com/projects#filter"
driver.get(url)
time.sleep(3)

loadAllButton = driver.find_element_by_xpath("//button[normalize-space()='View All']")
loadAllButton.click()
time.sleep(5)

content = driver.page_source
soup = BeautifulSoup(content, 'html.parser')
nodes = soup.findAll('a', {'title':'Go to GitHub'})

orgs = []
for node in nodes:
    url = node.get('href')
    org = url.split('/')[3]
    if org not in orgs:
        orgs.append(org)
        