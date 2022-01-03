# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from selenium import webdriver  
from bs4 import BeautifulSoup
import time

driver_path = "/Users/erinnsun/Desktop/web_scraper/chromedriver"
driver = webdriver.Chrome(driver_path)

url = "https://opensource.oracle.com/"
driver.get(url)
print(len(driver.page_source))
while True:
    try:
        # loadMoreButton = driver.find_element_by_xpath("//button[contains(@aria-label,'Load More')]")
        loadMoreButton = driver.find_element_by_xpath("//button[@id='load-more']")
        loadMoreButton.click()
        time.sleep(1)
        print(len(driver.page_source))
    except Exception as e:
        print(e)
        break


content = driver.page_source
soup = BeautifulSoup(content, 'html.parser')
nodes = soup.findAll("a", {"class": "gh-Repo-MetaItem gh-Repo-MetaItem--rating template-href"})

orgs = []
for node in nodes:
    org = node.get("href").split('/')[-1]
    if org not in orgs:
        orgs.append(org)