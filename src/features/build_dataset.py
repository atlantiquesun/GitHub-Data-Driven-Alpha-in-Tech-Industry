#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 21:24:59 2021

@author: erinnsun
"""

import pandas as pd
from dateutil.relativedelta import relativedelta

from sklearn.preprocessing import MinMaxScaler



def build_dataset(start_company = 0, end_company = 82, exclude_companies = [],
                     start_month = "9/01/2010", end_month = "4/01/2021",
                     company_path = "../../data/companies.csv", 
                     git_data_path = "../../data/intermediate/github_data/",
                     fin_data_path = "../../data/intermediate/financial_data/",
                     processed_data_path = "../../data/processed/"
                     ):
  
  
  start_month = pd.to_datetime(start_month)
  end_month = pd.to_datetime(end_month)

  companies = pd.read_csv(company_path, sep = ";")
  df_complete = None
  for i in range(start_company, end_company):

    company_git = companies.at[i, 'githubUser']
    if (company_git in exclude_companies):
      continue

    company_name = companies.at[i, "shortName"]
    company_ticker = companies.at[i, "symbol"]
    # print(i, company_git, company_name)
    
    months = pd.date_range(start = start_month, end = end_month + relativedelta(months = 1), freq = 'M')
    months = [x + relativedelta(days = 1) - relativedelta(months = 1) for x in months]
    df = pd.DataFrame(index = months)
    df_git = pd.read_csv(git_data_path + company_git + ".csv", index_col = 0)
    df_fin = pd.read_csv(fin_data_path + company_ticker + ".csv", index_col = 0)

    # select months
    df_git["month_start"] = pd.to_datetime(df_git["month_start"])
    df_fin["month_start"] = pd.to_datetime(df_fin["month_start"])
    df_git["month_end"] = pd.to_datetime(df_git["month_end"])
    df_fin["month_end"] = pd.to_datetime(df_fin["month_end"])
    df_git = df_git.loc[(df_git["month_start"] >= start_month) & (df_git["month_start"] <= end_month)]
    df_fin = df_fin.loc[(df_fin["month_start"] >= start_month) & (df_fin["month_start"] <= end_month)]

    # concatenate GitHub data and stock data
    df_git.index = df_git["month_start"]
    df_fin.index = df_fin["month_start"]
    df = pd.concat([df, df_git, df_fin], axis = 1)
    df.drop(columns=["month_end", "month_start"], inplace=True)
    df.dropna(inplace = True) # drop rows with missing data
    df["month_start"] = df.index
    df["githubUser"] = company_git
    df["ticker"] = company_ticker

    
    # concatenate to df_complete
    if (df_complete is None):
      df_complete = df
    else:
      df_complete = pd.concat([df_complete, df])

  df_complete.reset_index(drop = True, inplace = True)
  df_complete.to_csv(processed_data_path + "df.csv")
  return df_complete


'''

if __name__ == "__main__":
    df = build_dataset(start_company=0, end_company=82, exclude_companies=["microsoft", "facebook", "google", "westerndigitalcorporation", "xilinx"])

'''
