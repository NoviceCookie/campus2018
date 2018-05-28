import os
import pandas as pd
import numpy as np
import datetime
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import Lasso
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.model_selection import RandomizedSearchCV, GridSearchCV
from xgboost.sklearn import XGBRegressor
train_data = pd.read_csv("/home/tanyx/dataDemo/campus2018/holiday_fix_diff_all.csv")
test_data = pd.read_csv("/home/tanyx/dataDemo/campus2018/test.csv")
X = train_data[train_data["month"]>8].loc[:,["loc_id","month","day","hour","week_day"]].values
y = train_data[train_data["month"]>8]["num_of_people"].values
X_val = test_data.loc[:,["loc_id","month","day","hour","week_day"]].values
enc = OneHotEncoder()
enc.fit(np.vstack((X,X_val)))
X_one = enc.transform(X)
X_val_one = enc.transform(X_val)
X_train, X_test, y_train, y_test = train_test_split(X_one, y, test_size=0.1, random_state=0)
xlf = XGBRegressor(tive='reg:linear', learning_rate=0.07, n_estimators=700, nthread=4, min_child_weight=6, max_depth=16)
xlf.fit(X_train, y_train, eval_metric='rmse', verbose = True)

# 测试用
# xlf = XGBRegressor(tive='reg:linear', n_estimators=1000, nthread=4, min_child_weight=6, max_depth=16)
# parameters = {
#     "learning_rate":[0.18, 0.2, 0.22]
# }
# kr = GridSearchCV(xlf,param_grid=parameters, scoring="neg_mean_squared_error")
# kr.fit(X_one,y)


predicts = xlf.predict(X_test)
for i in range(len(predicts)):
    if predicts[i] < 0:
        predicts[i] = 0
print("RMSE:", np.sqrt(metrics.mean_squared_error(predicts, y_test)))

predicts = xlf.predict(X_val_one)
for i in range(len(predicts)):
    if predicts[i] < 0:
        predicts[i] = 0
test_data["num_of_people"] = predicts
test_data.to_csv("/home/tanyx/dataDemo/campus2018/result.csv",columns=["loc_id","time_stamp","num_of_people"], index=False, header=False)
test_data.to_csv("/home/tanyx/dataDemo/campus2018/result_total.csv", index=False)