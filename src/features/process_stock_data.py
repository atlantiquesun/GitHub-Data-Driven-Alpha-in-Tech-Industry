#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 21:17:21 2021

@author: erinnsun
"""


import pandas as pd
from dateutil.relativedelta import relativedelta



def process_stock_data(company_path = "../../data/companies.csv", 
                         data_path = "../../data/raw/financial_data/", 
                         results_path = "../../data/intermediate/financial_data/",
                         start_company = 0, end_company = 82, exclude_companies = [], 
                         start_month = "1/01/1999", end_month = "4/01/2021"):
  
  companies = pd.read_csv(company_path, sep = ";")

  for i in range(start_company, end_company):

    company_git = companies.at[i, 'githubUser']
    if (company_git in exclude_companies):
      continue

    company_name = companies.at[i, "shortName"]
    print(i, company_git, company_name)

    company_symbol = companies.at[i, "symbol"]

    df = pd.read_csv(data_path + company_symbol + ".csv")
    df.columns = [x.lower() for x in list(df.columns)]

    # group into monthly data
    df["date"] = pd.to_datetime(df["date"])
    df = df.groupby(pd.Grouper(key="date", freq="M")).nth([-1]) # take the last day in a month, indices are month-ends
    df["date"] = [x + relativedelta(days=1) - relativedelta(months=1) for x in list(df.index)] # get month-starts
    df = df.rename(columns={"date":"month_start"})
    df["month_end"] = df.index # get month-ends

    # calculate monthly return
    df["monthly_return"] = (df["close"] - df["close"].shift(1))/df["close"].shift(1)
    df.dropna(inplace=True)

    # select month range
    df = df.loc[(df['month_start'] >= pd.to_datetime(start_month)) & (df['month_start'] <= pd.to_datetime(end_month))]
    df.reset_index(drop=True, inplace=True)

    df.to_csv(results_path + company_git + ".csv")
    

'''

if __name__ == "__main__":
    process_stock_data(start_company=0, end_company=82)
    
'''