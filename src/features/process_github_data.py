#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 20:56:04 2021

@author: erinnsun
"""

import os
import requests

import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta


'''
1. Calculate cumulative data for each company (cumulate through repositories)
'''
def get_created_date(company_git, auth_token):

  query = """
  { 
    organization(login: "%s"){
      createdAt
    }
  }
  """%(company_git)

  response = requests.post('https://api.github.com/graphql', json={'query': query}, headers = {"Authorization": auth_token})
  if('data' not in response.json()):
    response = requests.get('https://api.github.com/orgs/' + company_git, headers={'Accept': "application/vnd.github.v3+json"})
    created_at = pd.to_datetime(response.json()['created_at']).replace(minute=0, second=0).tz_localize(None)
  else:
    created_at = pd.to_datetime(response.json()['data']['organization']['createdAt']).tz_localize(None)
  return created_at



def calculate_cumulative(auth_token,
                         company_path = "../../data/companies.csv", 
                         data_path = "../../data/raw/", 
                         cmlt_path = "../../data/intermediate/cumulative_data/",
                         start_company = 0, end_company = 82, exclude_companies = [], 
                         start_date = "1/01/1999", end_date = "9/01/2021",
                         ):
  '''
  auth_token: github api authorization token
  start: start company (index 0 to 82)
  end: end company (one past the last company to be processed)
  exclude_companies: GitHub usernames of the companies that need to be excluded (e.g. because of incomplete data)
  '''
  
  companies = pd.read_csv(company_path, sep = ";")
  data_cats = [] # data categories
  for name in os.listdir(data_path):
    if "History" in name: 
      data_cats.append(name)

  for i in range(start_company, end_company):

    company_git = companies.at[i, 'githubUser']
    if (company_git in exclude_companies):
      continue

    company_name = companies.at[i, "shortName"]
    print(i, company_git, company_name)

    # get the start date 
    created_at = get_created_date(company_git, auth_token)
    if(created_at > pd.to_datetime(start_date)):
      start_date = created_at

    # calculate the cumulative data for each category
    cmlt_data = {}
    cmlt_data["date"] = list(pd.date_range(start = start_date, end = end_date).tz_localize(None))   
    for category in data_cats:
      df = pd.read_csv(data_path + category + "/" + company_git + ".csv")
      df = df.rename(columns = {df.columns[0]: "date"})
      df["date"] = pd.to_datetime(df["date"])
      df = df.loc[(df["date"] >= pd.to_datetime(start_date)) & (df["date"] <= pd.to_datetime(end_date))]

      df.index = df["date"]
      df = df.drop(labels = "date", axis = 1)
      df["sum"] = df.sum(axis=1) #sum over the repositories for each date
      cmlt_data[category[:-len("History")]] = list(df["sum"])
  
    cmlt_data = pd.DataFrame(cmlt_data)
    cmlt_data.to_csv(cmlt_path + company_git + ".csv")









'''
2. Calculate monthly data 
'''
def process_github_data(company_path = "../../data/companies.csv", 
                         data_path = "../../data/intermediate/cumulative_data/", 
                         results_path = "../../data/intermediate/github_data/",
                         start_company = 0, end_company = 82, exclude_companies = [], 
                         start_month = "1/01/2010", end_month = "4/01/2021"):
  
  companies = pd.read_csv(company_path, sep = ";")

  for i in range(start_company, end_company):

    company_git = companies.at[i, 'githubUser']
    if (company_git in exclude_companies):
      continue

    company_name = companies.at[i, "shortName"]
    print(i, company_git, company_name)

    df = pd.read_csv(data_path + company_git + ".csv", index_col = 0)
    df['date'] = pd.to_datetime(df['date'])
    df = df.groupby(pd.Grouper(key="date", freq="M")).sum()
    df = df.drop(index=df.index[0], axis=0) # drop the first row because data in the first month might be incomplete

    # get month-starts and month-ends
    df['month_end'] = df.index
    month_starts = [x+datetime.timedelta(days=1)-relativedelta(months=1) for x in list(df['month_end'])]
    df['month_start'] = month_starts
    df.index = month_starts
    df = df.loc[(df['month_start'] >= pd.to_datetime(start_month)) & (df['month_start'] <= pd.to_datetime(end_month))]
    
    df.to_csv(results_path + company_git + ".csv")


'''

if __name__ == "__main__":
    auth_token = "token ghp_akehddksjhfksjfhkfh" # this token is invalid, only for demo purposes
    calculate_cumulative(auth_token, start_company = 0, end_company = 82, exclude_companies = ["microsoft", "facebook", "google", "westerndigitalcorporation", "xilinx"])
    process_github_data(start_company = 0, end_company = 82, exclude_companies = ["microsoft", "facebook", "google", "westerndigitalcorporation", "xilinx"])
    
'''