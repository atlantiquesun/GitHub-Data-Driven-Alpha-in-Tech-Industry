#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 30 23:47:42 2021

@author: erinnsun
"""

from selenium import webdriver  
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

driver_path = "/Users/erinnsun/Desktop/web_scraper/chromedriver"
driver = webdriver.Chrome(driver_path)

url = "https://opensource.newrelic.com/explore-projects/"
driver.get(url)
wait = WebDriverWait(driver, 20)
wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='explore-projects-module--show-all-button-container--1q4rq']/button[@type='button']"))).click()