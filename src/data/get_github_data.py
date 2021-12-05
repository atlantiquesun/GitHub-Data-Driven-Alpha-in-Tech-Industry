#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 22:25:35 2021

@author: erinnsun
"""

import pandas as pd
import requests
import time
import datetime

'''
1. GraphQL queries
'''
def generateForkQuery(owner, name, endCursor=None):
  if(endCursor is None):
    query = """
      { 
            repository(owner:"%s", name:"%s") { 
              forks(first: 100) {
                pageInfo {
                  endCursor
                  hasNextPage
                }
                nodes {
                  createdAt
                }
              }
            }
          }
    """%(owner, name)
    return query
  else: 
    query = """
            { 
              repository(owner:"%s", name:"%s") { 
                forks(first: 100, after:"%s") {
                  pageInfo {
                    endCursor
                    hasNextPage
                  }
                  nodes {
                    createdAt
                  }
                }
              }
            }
            """%(owner, name, endCursor)
    return query


def generateStarQuery(owner, name, endCursor=None):
  if(endCursor is None):
    query = """
      { 
            repository(owner:"%s", name:"%s") { 
              stargazers(first: 100) {
                pageInfo {
                  endCursor
                  hasNextPage
                }
                edges {
                  starredAt
                }
              }
            }
          }
    """%(owner, name)
    return query
  else:
    query = """
            { 
              repository(owner:"%s", name:"%s") { 
                stargazers(first: 100, after:"%s") {
                  pageInfo {
                    endCursor
                    hasNextPage
                  }
                  edges {
                    starredAt
                  }
                }
              }
            }
            """%(owner, name, endCursor)
    return query


def generateIssueQuery(owner, name, endCursor=None):
  if(endCursor is None):
    query = """
      {
      repository(owner: "%s", name: "%s") {
                issues(first: 100) {
                  pageInfo {
                    endCursor
                    hasNextPage
                  }
                  nodes {
                    closedAt
                    createdAt
                  }
                }
              }
    }
    """%(owner, name)
    return query
  else:
    query = """
      {
        repository(owner: "%s", name: "%s") {
                  issues(first: 100, after:"%s") {
                    pageInfo {
                      endCursor
                      hasNextPage
                    }
                    nodes {
                      closedAt
                      createdAt
                    }
                  }
                }
      }
    """%(owner, name, endCursor)
    return query


def getOID(owner, name, headers):
  #get object ID, prepare for fetching commit data
  query = """
    {
      repository(owner: "%s", name: "%s") {
            defaultBranchRef {
              target {
                ... on Commit {
                  oid
                  committedDate
                  history {
                    totalCount
                  }
                }
              }
            }
          }
      }
  """%(owner, name)
  response = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
  if 'data' not in response.json().keys():
    print(response.content)
  if(response.json()['data']['repository']['defaultBranchRef'] is None):
    return None
  oid = response.json()['data']['repository']['defaultBranchRef']['target']['oid']
  return oid


def generateCommitQuery(owner, name, oid, endCursor=None):
  if(endCursor is None):
    query = """
    {
    repository(owner: "%s", name: "%s") {
            object(oid: "%s") {
              ... on Commit {
                history(first: 100) {
                  totalCount
                  pageInfo {
                    endCursor
                    hasNextPage
                  }
                  nodes {
                    committedDate
                  }
                }
              }
            }
          }
      }
    """%(owner, name, oid)
    return query
  else:
    query = """
      {
      repository(owner: "%s", name: "%s") {
              object(oid: "%s") {
                ... on Commit {
                  history(first: 100, after: "%s") {
                    totalCount
                    pageInfo {
                      endCursor
                      hasNextPage
                    }
                    nodes {
                      committedDate
                    }
                  }
                }
              }
            }
        }
    """%(owner, name, oid, endCursor)
    return query

def generatePRQuery(owner, name, endCursor=None):
  if (endCursor is None):
    query = """
          { 
          repository(owner:"%s", name:"%s") { 
              pullRequests(first: 100){
                  pageInfo{
                    hasNextPage
                    endCursor
                  }
                  nodes{
                    createdAt
                    mergedAt
                    closedAt
                  }
                        
                }
                    }
              }
    """%(owner, name)
  else:
    query = """
          { 
          repository(owner:"%s", name:"%s") { 
              pullRequests(first: 100, after:"%s"){
                  pageInfo{
                    hasNextPage
                    endCursor
                  }
                  nodes{
                    createdAt
                    mergedAt
                    closedAt
                  }
                        
                }
                    }
              }
    """%(owner, name, endCursor)
  return query



'''
2. Retrieve Data from GitHub API
'''

def processNode(x, category, closed=False, merged=False):
  '''
  return the date (year-month-day) in a record
  '''
  if (category == "star"):
    return x["starredAt"][:10]   
  elif (category == "fork"):
    return x["createdAt"][:10]
  elif (category == "commit"):
    return x["committedDate"][:10]
  elif (category == "issue" and closed):
    if x["closedAt"] is None:
      return None
    else:
      return x["closedAt"][:10]
  elif (category == "issue" and not closed):
    return x["createdAt"][:10]
  elif (category == "pullRequest" and merged):
    if x["mergedAt"] is None: 
      return None
    else:
      return x["mergedAt"][:10]
  elif (category == "pullRequest" and closed):
    if x["closedAt"] is None:
      return None
    else:
      return x["closedAt"][:10]
  elif (category == "pullRequest" and not closed):
    return x["createdAt"][:10]
  else:
    print("Invalid category")
    return



def categoryExtension(category):
    if(category == "star"):
      return "stargazers"
    else:
      return category+'s'
  
    
  
class History():
  def __init__(self, company, normalizedName):
    self.headers = {"Authorization": "token sdf_sdkhfgsegrwygk3hkgh42k"} # invalid token, only for demo purposes
    self.categories = ("star", "fork", "commit", "issue", "pullRequest")

    self.company = None
    self.normalizedName = None

    self.repos = None
    self.anomalyTracker = None
  
    self.historyDict = None
    self.set_company(company, normalizedName)
  
  def set_company(self, company, normalizedName):
    self.company = company
    self.normalizedName = normalizedName

    self.repos = None
    self.repo_list()
    self.anomalyTracker = None
    
    self.start_date = pd.to_datetime("1/01/1999")
    self.end_date = pd.to_datetime('11/01/2021')

    dates = list(pd.date_range(start="1/01/1999", end='11/01/2021')) 
    repos = [x[0] for x in self.repos]
    self.historyDict = {"star": pd.DataFrame(index = dates, columns = repos), "fork": pd.DataFrame(index = dates, columns = repos)
    , "commit": pd.DataFrame(index = dates, columns = repos), "issueClosed":pd.DataFrame(index = dates, columns = repos),
    "issue":pd.DataFrame(index = dates, columns = repos), "pullRequest":pd.DataFrame(index = dates, columns = repos), 
    "pullRequestClosed": pd.DataFrame(index = dates, columns = repos), "pullRequestMerged": pd.DataFrame(index = dates, columns = repos)} 
     #"issue" = "issueCreated", "pullRequest" = "pullRequestCreated"

    for x in self.historyDict:
      self.historyDict[x] = self.historyDict[x].fillna(0)

  def repo_list(self):
    '''
    read the list of repos that the company owns
    '''
    
    self.repos = []
    nextPage = "https://api.github.com/users/"+self.company+"/repos?per_page=100"
    with requests.Session() as s:
      while (nextPage is not None):
        print(nextPage)
        response = s.get(nextPage)
        if("next" in response.links):
          nextPage = response.links['next']['url']
        else:
          nextPage = None
        data = response.json()
        for repo in data:
          oid = getOID(owner = self.company, name=repo['name'], headers=self.headers)
          if(oid is not None): #check that the repository is not empty
            self.repos.append((repo['name'], oid))

  
  def sleepMode(self, query):
    '''
    sleep for one hour, a notice each 10 minutes

    query: the last query that received a "api limit exceeded" notice (i.e. did not get a proper response)
    '''
    for i in range(1, 7):
      print("sleeping 10min:", i)
      time.sleep(600) # sleep 10 min

    response = requests.post('https://api.github.com/graphql', json={'query': query}, headers=self.headers)
    return response
    
  def generateQuery(self, category, repo, endCursor=None, oid=None):
    '''
    category: "star," "fork," "commit," "issue", "pullRequest"
    '''
    if (category == "fork"):
      return generateForkQuery(owner=self.company, name=repo, endCursor=endCursor)
    elif (category == "star"):
      return generateStarQuery(owner=self.company, name=repo, endCursor=endCursor)
    elif (category == "commit"):
      return generateCommitQuery(owner=self.company, name=repo, endCursor=endCursor, oid=oid)
    elif (category == "issue"):
      return generateIssueQuery(owner=self.company, name=repo, endCursor=endCursor)
    elif (category == "pullRequest"):
      return generatePRQuery(owner=self.company, name=repo, endCursor=endCursor)
    else:
      print("Invalid query category")
      return 
  
  def exportData(self, folder):
    for category in self.categories:
      self.exportCategory(category, folder)

  def exportCategory(self, category, folder):
    df = self.historyDict[category]
    address = folder+category+'History/'+self.company+'.csv'
    df.to_csv(address)

    if(category == "issue" or category == "pullRequest"):
      df = self.historyDict[category+"Closed"]
      address = folder+category+'ClosedHistory/'+self.company+'.csv'
      df.to_csv(address)
    
    if(category == "pullRequest"):
      df = self.historyDict["pullRequestMerged"]
      address = folder+'pullRequestMergedHistory/'+self.company+'.csv'
      df.to_csv(address)

  def addData(self, folder='../../data/raw/'):
    start_cat = 0 # start with star data
    if(self.company == "xilinx"): 
        start_cat = 2 
        
    for category in self.categories[start_cat:]:
      for (repo, oid) in self.repos:
        self.addCategory(category, repo, oid)
      self.exportCategory(category, folder) 

  def addCategory(self, category, repo, oid, start_page=1):
    print("Processing "+category+" data of "+self.company+"/"+repo)

    nodes = []
    endCursor = None
    hasNextPage = True

    page_count = 0
    with requests.Session() as s:
      while(hasNextPage):
        page_count += 1
        print(page_count)
        query = self.generateQuery(category = category, repo=repo, endCursor=endCursor, oid=oid)
        response = s.post('https://api.github.com/graphql', json={'query': query}, headers=self.headers)

        self.anomalyTracker = response #to print out the content when the program accidentally stops
        while (response.json() is None or 'data' not in response.json().keys()): #not a proper response (e.g. api limit exceeded)
          print(self.company)
          response = self.sleepMode(query)

        if (category == "commit"):
          data = response.json()['data']['repository']['object']['history']
        else:
          data = response.json()['data']['repository'][categoryExtension(category)]
        
        endCursor = data['pageInfo']['endCursor']
        hasNextPage = data['pageInfo']['hasNextPage']
        if(page_count < start_page): 
          continue

        if category == "star":
          nodes.extend(data['edges'])
        else:
          nodes.extend(data['nodes'])
    
      for x in nodes:
        date1 = processNode(x=x, category=category, closed=True) #closed = True, merged=False
        date2 = processNode(x=x, category=category, closed=False)  
        date3 = processNode(x=x, category=category, merged=True)
        
        date2 = pd.to_datetime(date2)
        if (date2 >= self.start_date and date2 <= self.end_date):
            if (self.historyDict[category].at[date2, repo])==0:
              self.historyDict[category].at[date2, repo] = 1
            else:
              self.historyDict[category].loc[date2, repo] += 1
    
        if category == "issue" or category == "pullRequest": #need to add closedAt data
          if (date1 is not None): 
              date1 = pd.to_datetime(date1)
              if (date1 >= self.start_date and date1 <= self.end_date):
                  if (self.historyDict[category+"Closed"].at[date1, repo])==0:
                    self.historyDict[category+"Closed"].at[date1, repo] = 1
                  else:
                    self.historyDict[category+"Closed"].at[date1, repo] += 1

        
        if category == "pullRequest": #need to add mergedAt data
          if (date3 is not None): 
            date3 = pd.to_datetime(date3)
            if (date3 >= self.start_date and date3 <= self.end_date):
                if (self.historyDict[category+"Merged"].at[date3, repo])==0:
                  self.historyDict[category+"Merged"].at[date3, repo] = 1
                else:
                  self.historyDict[category+"Merged"].at[date3, repo] += 1


if __name__ == "__main__":
    company_path = "../../data/companies.csv"
    company_info = "../input/company-info/companies_final.csv"
    df = pd.read_csv(company_info, sep=";")
    
    h = None
    for i in range(0, df.shape[0]):
      company = df.at[i, 'githubUser']
      normalizedName = df.at[i, "shortName"]
      if h is None:
        h = History(company, normalizedName)
      else:
        h.set_company(company, normalizedName)
      h.addData()
