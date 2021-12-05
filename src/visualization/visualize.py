#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 22:00:24 2021

@author: erinnsun
"""

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

'''
1. Compare portfolio return
'''

def _long_only_strategy_monthly(df_predict_return, tic_monthly_return, trade_month, top_quantile_threshold=0.75):
    long_dict = {}
    for i in range(df_predict_return.shape[0]):
        top_q = df_predict_return.iloc[i].quantile(top_quantile_threshold)
        # low_q=df_predict_return.iloc[i].quantile(0.2)
        # Select all stocks
        # long_dict[df_predict_return.index[i]] = df_predict_return.iloc[i][~np.isnan(df_predict_return.iloc[i])]
        # Select Top 30% Stocks
        long_dict[df_predict_return.index[i]] = df_predict_return.iloc[i][df_predict_return.iloc[i] >= top_q]
        # short_dict[df_predict_return.index[i]] = df_predict_return.iloc[i][df_predict_return.iloc[i]<=low_q]

    portfolio_return_dic = {}
    for i in range(len(trade_month)):
        # for longX_train_rf only
        # calculate weight based on predicted return
        long_normalize_weight = long_dict[trade_month[i]] / sum(long_dict[trade_month[i]].values)
        # map date and tic
        long_tic_return = tic_monthly_return[tic_monthly_return.index == trade_month[i]][
            long_dict[trade_month[i]].index]
        # return * weight
        long_return_table = long_tic_return * long_normalize_weight
        portfolio_return_dic[trade_month[i]] = long_return_table.values.sum()

        # for short only
        # short_normalize_weight=short_dict[trade_month[i]]/sum(short_dict[trade_month[i]].values)
        # short_tic_return=tic_monthly_return[tic_monthly_return.index==trade_month[i]][short_dict[trade_month[i]].index]
        # short_return_table=short_tic_return
        # portfolio_return_dic[trade_month[i]] = long_return_table.values.sum() + short_return_table.values.sum()

    df_portfolio_return = pd.DataFrame.from_dict(portfolio_return_dic, orient='index')
    df_portfolio_return = df_portfolio_return.reset_index()
    df_portfolio_return.columns = ['trade_month', 'monthly_return']
    df_portfolio_return.index = df_portfolio_return.trade_month
    df_portfolio_return = df_portfolio_return['monthly_return']
    return df_portfolio_return



def get_monthly_return(trade_months, 
                       unique_ticker,
                       fin_data_path = "../../data/intermediate/financial_data/"):
  '''
  returns:
    monthly_return: pd.DataFrame
      index = trade_months, columns = unique_ticker, may contain NaN 
  '''
  # get the monthly return of each stocks
  monthly_return = pd.DataFrame(index=trade_months)
  monthly_return.index.name = "month_start"
  monthly_return.index = pd.to_datetime(monthly_return.index)

  for company in unique_ticker:
    df_temp = pd.read_csv(fin_data_path + company +'.csv')
    df_temp['month_start'] = pd.to_datetime(df_temp['month_start'])
    df_temp = df_temp.loc[(df_temp['month_start'] >= trade_months[0]) & (df_temp['month_start'] <= trade_months[-1])]
    df_company = pd.DataFrame(df_temp['monthly_return'].values, index = df_temp['month_start'], columns=[company])
    monthly_return = pd.concat([monthly_return, df_company], axis = 1)
    


def show_portfolio_return(trade_months,
                          unique_ticker,
                          top_quantile_threshold = 0.75,
                          result_path = '../../results/'):
    
    df_monthly_return = get_monthly_return(trade_months, unique_ticker)
    
    # load results
    df_predict_lr = pd.read_csv(result_path + "lr.csv", index_col = 0)
    df_predict_lasso = pd.read_csv(result_path + "lasso.csv", index_col = 0)
    df_predict_ridge = pd.read_csv(result_path + "ridge.csv", index_col = 0)
    df_predict_rf = pd.read_csv(result_path + "rf.csv", index_col = 0)
    df_predict_svm = pd.read_csv(result_path + "svm.csv", index_col = 0)
    df_predict_gbm = pd.read_csv(result_path + "gbm.csv", index_col = 0)
    df_predict_ada = pd.read_csv(result_path + "ada.csv", index_col = 0)
    df_predict_lstm = pd.read_csv(result_path + "lstm.csv", index_col = 0)
    df_predict_best = pd.read_csv(result_path + "best.csv", index_col = 0)
    
    # convert indices to datetime objects
    df_predict_lr.index = pd.to_datetime(df_predict_lr.index)
    df_predict_lasso.index = pd.to_datetime(df_predict_lasso.index)
    df_predict_ridge.index = pd.to_datetime(df_predict_ridge.index)
    df_predict_rf.index = pd.to_datetime(df_predict_rf.index)
    df_predict_svm.index = pd.to_datetime(df_predict_svm.index)
    df_predict_gbm.index = pd.to_datetime(df_predict_gbm.index)
    df_predict_ada.index = pd.to_datetime(df_predict_ada.index)
    df_predict_lstm.index = pd.to_datetime(df_predict_lstm.index)
    df_predict_best.index = pd.to_datetime(df_predict_best.index)
    
    # calculate portfolio return
    df_portfolio_return_lr = _long_only_strategy_monthly(df_predict_lr, df_monthly_return, trade_months, top_quantile_threshold)
    df_portfolio_return_lasso = _long_only_strategy_monthly(df_predict_lasso, df_monthly_return, trade_months, top_quantile_threshold)
    df_portfolio_return_ridge = _long_only_strategy_monthly(df_predict_ridge, df_monthly_return, trade_months, top_quantile_threshold)
    df_portfolio_return_rf    = _long_only_strategy_monthly(df_predict_rf,   df_monthly_return, trade_months, top_quantile_threshold)
    df_portfolio_return_svm   = _long_only_strategy_monthly(df_predict_svm,  df_monthly_return, trade_months, top_quantile_threshold)
    df_portfolio_return_gbm    = _long_only_strategy_monthly(df_predict_gbm,   df_monthly_return, trade_months, top_quantile_threshold)
    df_portfolio_return_ada   = _long_only_strategy_monthly(df_predict_ada,  df_monthly_return, trade_months, top_quantile_threshold)
    df_portfolio_return_lstm  = _long_only_strategy_monthly(df_predict_lstm, df_monthly_return, trade_months, top_quantile_threshold)
    df_portfolio_return_best  = _long_only_strategy_monthly(df_predict_best, df_monthly_return,trade_months, top_quantile_threshold)
    
    # calculate baseline (equal portfolio return)
    selected_monthly_return = df_monthly_return[unique_ticker]
    equally_portfolio_return=[]
    for i in range(len(trade_months)):
        return_remove_nan = selected_monthly_return.iloc[i][~np.isnan(df_monthly_return.iloc[i])] 
        equally_portfolio_return.append(sum(return_remove_nan)/len(return_remove_nan))
    
    df_equally_portfolio_return=pd.DataFrame(equally_portfolio_return, index = trade_months, columns = ['monthly_return'])
    
    # plot the figure
    fig, ax = plt.subplots(figsize=(15,10))
    baseline = ((df_equally_portfolio_return+1).cumprod()-1).plot(ax=ax, c='black',label='baseline')
    ridge = ((df_portfolio_return_ridge+1).cumprod()-1).plot(ax=ax, c='b',label='ridge')
    lasso = ((df_portfolio_return_lasso+1).cumprod()-1).plot(ax=ax, c='gold',label='lasso')
    rf = ((df_portfolio_return_rf+1).cumprod()-1).plot(ax=ax, c='plum',label='random forest')
    svm = ((df_portfolio_return_svm+1).cumprod()-1).plot(ax=ax, c='green',label='svm')
    gbm = ((df_portfolio_return_gbm+1).cumprod()-1).plot(ax=ax, c='c',label='gbm')
    ada = ((df_portfolio_return_ada+1).cumprod()-1).plot(ax=ax, c='m',label='ada')
    lstm = ((df_portfolio_return_lstm+1).cumprod()-1).plot(ax=ax, c='purple',label='lstm')
    best = ((df_portfolio_return_best+1).cumprod()-1).plot(ax=ax, c='r',label='best')
    plt.legend()
    plt.title('Cumulative Return', {'size':16})
    plt.show()



'''

if __name__ == "__main__":
    df = build_dataset(start_company=0, end_company=82, exclude_companies=["microsoft", "facebook", "google", "westerndigitalcorporation", "xilinx"])
    trade_months, unique_ticker = train(df)
    show_portfolio_return(trade_months, unique_ticker)
    
'''