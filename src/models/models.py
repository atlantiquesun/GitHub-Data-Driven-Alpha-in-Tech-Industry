'''
Component Learners
1.   lr: linear regression
2.   rfe: recursive feature elimination with linear regression
3.   lasso: lasso regression
4.   ridge: ridge regression
5.   rf: random forest regression
6.   svm: support vector machine
7.   gbm: gradient boosting machine
8.   ada: AdaBoost regression with decision tree
9.   lstm: long short-term memory networks
'''

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.svm import SVR
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import cross_val_score, cross_val_predict
from sklearn.linear_model import Ridge

from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import AdaBoostRegressor

from sklearn.model_selection import TimeSeriesSplit, GridSearchCV,RandomizedSearchCV

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout





def train_linear_regression(X_train,y_train):

    lr_regressor = LinearRegression()
    model = lr_regressor.fit(X_train, y_train)
    
    return model


def train_recursive_feature_elimination(X_train,y_train):

    lr_regressor = LinearRegression(random_state = 42)
    model = RFE(lr_regressor)
    
    return model


def train_lasso(X_train, y_train):
  
    lasso = Lasso()
    # scoring_method = 'r2'
    # scoring_method = 'explained_variance'
    scoring_method = 'neg_mean_absolute_error'
    # scoring_method = 'neg_mean_squared_error'
    # scoring_method = 'neg_mean_squared_log_error'
    parameters = {'alpha': [1e-15, 1e-10, 1e-8, 1e-4, 1e-3, 1e-2, 1, 5, 10, 20],
                  'tol': [1e-4, 1e-3, 1e-2, 1e-1]} # vary regularization 
    lasso_regressor = GridSearchCV(lasso, parameters, scoring=scoring_method, cv=3)
    lasso_regressor.fit(X_train, y_train)

    model = lasso_regressor.best_estimator_
    return model



def train_ridge(X_train, y_train):

    ridge = Ridge()
    # scoring_method = 'r2'
    # scoring_method = 'explained_variance'
    scoring_method = 'neg_mean_absolute_error'
    # scoring_method = 'neg_mean_squared_error'
    # scoring_method = 'neg_mean_squared_log_error'
    parameters = {'alpha': [1e-15, 1e-10, 1e-8, 1e-4, 1e-3, 1e-2, 1, 5, 10, 20],  
                  'tol': [1e-4, 1e-3, 1e-2, 1e-1]} 
    ridge_regressor = GridSearchCV(ridge, parameters, scoring=scoring_method, cv=3)
    ridge_regressor.fit(X_train, y_train)

    model = ridge_regressor.best_estimator_
    return model



def train_random_forest(X_train, y_train):
  
    # randomforest_regressor = RandomForestRegressor(n_estimators = 500, max_features=6)
    # model = randomforest_regressor.fit(X_train, y_train)

    random_grid = {'bootstrap': [True, False],
                   'max_depth': [10, 20, 40, 80, 100, None],
                   'max_features': ['auto', 'sqrt'],
                   'min_samples_leaf': [1, 2, 5, 10],
                   'min_samples_split': [2, 5, 10],
                   'n_estimators': [50, 200, 400, 600, 800, 1500]}
    
    rf = RandomForestRegressor(random_state=42)
    randomforest_regressor = RandomizedSearchCV(estimator=rf, param_distributions=random_grid,
                                                cv=3, n_jobs=-1, scoring='neg_mean_absolute_error', verbose=0)
    randomforest_regressor.fit(X_train, y_train)
    model = randomforest_regressor.best_estimator_
    
    return model



def train_svm(X_train, y_train):

    svr = SVR()

    # param_grid_svm = {'C':[0.001, 0.01, 0.1, 1, 10],'gamma': [1e-7, 1e-4,0.001,0.1]}
    param_grid_svm = {'kernel': ('linear', 'rbf','poly'), 'C':[0.001, 0.01, 0.1, 1, 10],'gamma': [1e-7, 1e-4,0.001,0.1],'epsilon':[0.1,0.2,0.5,0.3]}

    # scoring_method = 'r2'
    # scoring_method = 'explained_variance'
    scoring_method = 'neg_mean_absolute_error'
    # scoring_method = 'neg_mean_squared_error'
    # scoring_method = 'neg_mean_squared_log_error'
    
    svm_regressor = GridSearchCV(estimator=svr, param_grid=param_grid_svm,
                                       cv=3, n_jobs=-1, scoring=scoring_method, verbose=0)

    svm_regressor.fit(X_train, y_train)
    model = svm_regressor.best_estimator_

    return model



def train_gbm(X_train, y_train):
    '''
    gbm = GradientBoostingRegressor(random_state=42)
    # model = gbm.fit(X_train, y_train)
    param_grid_gbm = {'learning_rate': [0.1, 0.05, 0.01, 0.001], 'n_estimators': [100, 250, 500, 1000]}
    # scoring_method = 'r2'
    # scoring_method = 'explained_variance'
    scoring_method = 'neg_mean_absolute_error'
    # scoring_method = 'neg_mean_squared_error'
    #scoring_method = 'neg_mean_squared_log_error'
    gbm_regressor = RandomizedSearchCV(estimator=gbm, param_distributions=param_grid_gbm,
                                       cv=3, n_jobs=-1, scoring=scoring_method, verbose=0)
    gbm_regressor.fit(X_train, y_train)
    model = gbm_regressor.best_estimator_
    '''
    
    gbm_regressor = GradientBoostingRegressor()
    model = gbm_regressor.fit(X_train, y_train)

    return model




def train_ada(X_train, y_train):
    ada = AdaBoostRegressor(random_state=1)

    # model = ada.fit(X_train, y_train)

    param_grid_ada = {'n_estimators': [20, 50, 100],
                      'learning_rate': [0.01, 0.05, 0.1, 0.3, 1],
                      'loss' : ['linear', 'square', 'exponential']
                     
                     }
    # scoring_method = 'r2'
    # scoring_method = 'explained_variance'
    scoring_method = 'neg_mean_absolute_error'
    # scoring_method = 'neg_mean_squared_error'
    #scoring_method = 'neg_mean_squared_log_error'

    ada_regressor = GridSearchCV(estimator=ada, param_grid=param_grid_ada, cv=3, n_jobs=-1, scoring=scoring_method, verbose=0)

    ada_regressor.fit(X_train, y_train)
    model = ada_regressor.best_estimator_
    
    return model



def train_lstm(X_train, y_train):
    
    # Initialising the RNN
    regressor = Sequential()
    
    # Adding the first LSTM layer and some Dropout regularisation
    regressor.add(LSTM(units = 80, return_sequences = True, input_shape = (X_train.shape[1], X_train.shape[2])))
    regressor.add(Dropout(0.2))

    # Adding a second LSTM layer and some Dropout regularisation
    regressor.add(LSTM(units = 40, return_sequences = True))
    regressor.add(Dropout(0.2))

    # Adding a third LSTM layer and some Dropout regularisation
    regressor.add(LSTM(units = 20, return_sequences = False))
    regressor.add(Dropout(0.2))

    # Adding a fourth LSTM layer and some Dropout regularisation
    #regressor.add(LSTM(units = 20,return_sequences = False))
    #regressor.add(Dropout(0.2))

    # Adding the output layer
    regressor.add(Dense(units = 1, activation='linear'))
    
    #scoring_method = 'neg_mean_absolute_error'
    # scoring_method = 'neg_mean_squared_error'
    #scoring_method = 'neg_mean_squared_log_error'
    # Compiling the RNN
    regressor.compile(optimizer = 'adam', loss = 'mean_absolute_error')

    # Fitting the RNN to the Training set
    regressor.fit(X_train, y_train, epochs = 8, batch_size = 32)
    #print(regressor.summary())
    return regressor




