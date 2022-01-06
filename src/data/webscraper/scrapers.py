#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  3 15:42:47 2022

@author: erinnsun
"""

# for web scraping
from selenium import webdriver  
from bs4 import BeautifulSoup
import time
import re
import requests

# for file IO
import pandas as pd
import json


def get_org(git_url):
    '''
    utility function: retrieve an organization name from a 'git_url' of the form http://www.github.com/apple?=.github
    '''
    
    full = git_url.split('/')[3]
    return full.split('?')[0] # discard the repository name





def get_orgs_amzn(driver):
    page = requests.get("https://amzn.github.io/")
    lines = page.text.split('\n')

    flag = False
    orgs = []
    for line in lines:
        if (not flag and "Amazon GitHub Organizations" in line):
            flag = True
        elif flag:
            # example line: "<a href="https://github.com/alexa-labs">Alexa Labs</a> |"
            if("github.com/" in line):
                start = line.find("github.com/") + len("github.com/")
                end = line.find(">") - 1
                orgs.append(line[start:end])
                
    return orgs




def get_orgs_adobe(driver):
    
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
    
    return orgs




def get_orgs_apple(driver):
    
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
    for url in urls:
        content = requests.get(url).text
        soup = BeautifulSoup(content, 'html.parser')
        buttons = soup.findAll('a', {'class': 'button button-neutral button-reduced'})
        
        for b in buttons:
            if(b.find(text=re.compile("GitHub"))):
                org = get_org(b.get('href'))
                if(org not in orgs):
                    orgs.append(org)
    
    return orgs




def get_orgs_autodesk(driver):
    
    content = requests.get("https://autodesk.github.io/").text

    lines = content.split('\n')
    
    orgs = []
    for line in lines:
        if('var orgs =' in line):
            start = line.find('[')
            end = line.find(']')
            line = line[start+1 : end]
            orgs = line.split(',')
            orgs = [x[1:-1] for x in orgs]
            break  
    
    return orgs




def get_orgs_cerner(driver):
    
    content = requests.get("https://engineering.cerner.com/open-source/").text
    soup = BeautifulSoup(content, "html.parser")
    
    nodes = soup.findAll('div', {'class': 'col-sm'})
    orgs = []
    
    for n in nodes:
        if(len(n.findAll('a')) == 2): # if it is a normal open source project
            url = n.findAll('a')[0].get('href')
            org = url.split('/')[3]
            if(org not in orgs):
                orgs.append(org)  
    
    return orgs



def get_orgs_epam(driver):
    
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
    
    return orgs





def get_orgs_ericsson(driver):
    return ['EricssonResearch', 'Ericsson']





def get_orgs_facebook(driver):
    
    url = "https://opensource.fb.com/projects#filter"
    driver.get(url)
    time.sleep(5)
    
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
    
    return orgs




def get_orgs_ibm(driver):
    
    content = requests.get('https://raw.githubusercontent.com/IBM/ibm.github.io/85002f387daa2fadde5974b70629b12a26c8888c/js/orgs.js').text
    lines = content.split('\n')
    
    orgs = []
    for line in lines:
        if('name' in line):
            full_path = line.split(':')[1]
            if('/' not in full_path): # if it is an organization name
                org = full_path[2:-2]
            else: # ignore repositories
                continue
            if(org not in orgs):
                orgs.append(org)
    
    return orgs




def get_orgs_microsoft(driver):
    
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
    
    return orgs





def get_orgs_newrelic(driver):
    
    return ['newrelic', 'newrelic-experimental'] # excluding 'GlobalsoftWigilabs' because it is belongs to a partner of New Relic
    
    url = "https://opensource.newrelic.com/explore-projects/"
    driver.get(url)
    time.sleep(5)
    loadAllButton = driver.find_element_by_xpath("//div[@class='explore-projects-module--show-all-button-container--1q4rq']/button")
    loadAllButton.click()

    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')
    nodes = soup.findAll('a', {'class': 'explore-projects-module--project-container--2COfC'})

    orgs = []
    base_url = "https://opensource.newrelic.com"
    for node in nodes:
        project_url = node.get('href')
        driver.get(base_url + project_url)
        print(project_url)
        content = driver.page_source
        soup = BeautifulSoup(content, 'html.parser')
        try:
            url = soup.findAll('a', {'class':'css-rqim9w e132irl20'})[0].get('href')
        except IndexError:
            time.sleep(3)
            content = driver.page_source
            soup = BeautifulSoup(content, 'html.parser')
            url = soup.findAll('a', {'class':'css-rqim9w e132irl20'})[0].get('href')
        org = url.split('/')[3]
        if org not in orgs:
            orgs.append(org)
    
    # return orgs





def get_orgs_oracle(driver):
    
    url = "https://opensource.oracle.com/"
    driver.get(url)
    print(len(driver.page_source))
    while True:
        try:
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
    
    return orgs




def get_orgs_pinterest(driver):
    return ['pinterest', 'texturegroup']




def get_orgs_spotify(driver):
    
    content = requests.get('https://spotify.github.io/').text
    soup = BeautifulSoup(content, 'html.parser')
    nodes = soup.findAll('div', {'class': 'col-sm-6 col-lg-3'})
    
    orgs = []
    for node in nodes:
        url = node.findAll('a')[0].get('href')
        org = url.split('/')[3]
        if org not in orgs:
            orgs.append(org)
    
    return orgs





def get_orgs_twilio(driver):
    
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
    
    return orgs





def get_orgs_twitter(driver):
    
    content = requests.get('https://opensource.twitter.dev/projects/').text
    soup = BeautifulSoup(content, 'html.parser')
    
    nodes = soup.findAll('div', {'class':'project-card'})
    
    orgs = []
    for node in nodes:
        url = node('a', text=re.compile(r'GitHub'))[0].get('href')
        org = url.split('/')[3]
        if(org not in orgs):
            orgs.append(org)
    
    return orgs





def get_orgs_uber(driver):
    
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
    
    return orgs





def get_orgs_vmware(driver):
    return ['vmware', 'vmware-labs', 'vmware-samples', 'vmware-tanzu', 'vmware-tanzu-labs']





def get_orgs_wayfair(driver):
    
    url = "https://wayfair.github.io/"
    content = requests.get(url).text
    soup = BeautifulSoup(content, 'html.parser')
    sections = soup.findAll('div', {'class': 'd-inline-block'})

    for s in sections:
        heading = s.findAll('div', {'class': 'footer-heading'})[0]
        if(heading.text == 'GitHub'):
            nodes = s.findAll('a')

    orgs = []
    for node in nodes:
        url = node.get('href')
        org = url.split('/')[3]
        if org not in orgs:
            orgs.append(org)
    
    return orgs
   
 


def get_orgs_baidu(driver):
    
    return ['ApolloAuto', 'PaddlePaddle', 'baidu', 'xuperchain', 'swan-team'] # to be efficient

    url = "https://opensource.baidu.com/#/projectslist"
    driver.get(url)
    time.sleep(3)

    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')
    body = soup.findAll('div', {'class': 'projectsList'})[0]
    nodes = body.findAll('a')

    # get the number of pages
    footer = soup.findAll('ul', {'class':'pagination'})[0]
    page_elements = footer.findAll('li')
    pages = list(range(2, len(page_elements)-2))
    pages = [str(x) for x in pages]
    pages.append("尾页")

    for page in pages:
        
        # find the page 'i' button and click it
        btn = driver.find_element_by_link_text(page)
        time.sleep(5)
        btn.click()
        time.sleep(2)
        
        # add the new nodes
        content = driver.page_source
        soup = BeautifulSoup(content, 'html.parser')
        body = soup.findAll('div', {'class': 'projectsList'})[0]
        nodes.extend(body.findAll('a'))

    orgs = []
    for node in nodes:
        url = node.get('href')
        org = url.split('/')[3]
        if org not in orgs:
            orgs.append(org)
    
    return orgs




def get_orgs_atlassian(driver):
    
    return ['atlassian', 'atlassian-labs']




def get_orgs_vonage(driver):
    
    return ['vonage', 'nexmo']




if __name__ == '__main__':
    
    companies_path = "./companies_final.csv"
    companies = pd.read_csv(companies_path, sep = ",")
    
    driver_path = "./chromedriver"
    driver = webdriver.Chrome(driver_path)
    
    d_orgs = {}
    for i in range(companies.shape[0]):
        company_git = companies.at[i, 'githubUser']
        company_ticker = companies.at[i, 'symbol']
        print(company_git)
        
        if(companies.at[i, 'multiple_orgs'] == '0'): # only a single github org
            d_orgs[company_git] = {'ticker': company_ticker, 'orgs':[company_git]}
        else:
            if(companies.at[i, 'scraper'] == 1): # has a web scraper
                d_orgs[company_git] = {'ticker': company_ticker, 'orgs': []}
                d_orgs[company_git]['orgs'] = eval('get_orgs_'+ company_git.lower() + '(driver)')
                if company_git not in d_orgs[company_git]['orgs']:
                    d_orgs[company_git]['orgs'].append(company_git)
    
    
    save_path = "./companies.json"
    with open(save_path, 'w') as f:
        json.dump(d_orgs, f)
    
    
    
        
        
        
    