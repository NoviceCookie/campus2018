# -*- coding: utf-8 -*-

import pandas as pd
import datetime
import numpy as np
import os
from campus2018 import check_day
base_dir = "/home/tanyx/dataDemo/campus2018/not_date"

frames = []
for csv in os.listdir(base_dir):
    frames.append(pd.read_csv(os.path.join(base_dir, csv), sep=",", encoding="utf-8"))
frame = pd.concat(frames,ignore_index=True)
frame["datetime"] = frame.apply(lambda x: datetime.datetime.strptime(x["time_stamp"], "%Y-%m-%d %H"), axis=1)
frame["month"] = frame.apply(lambda x: x["datetime"].month, axis=1)
frame["day"] = frame.apply(lambda x: x["datetime"].day, axis=1)
frame["hour"] = frame.apply(lambda x: x["datetime"].hour, axis=1)
frame["week"] = frame.apply(lambda x: x["day"]//7, axis=1)
frame["week_day"] = frame.apply(lambda x: x["datetime"].weekday(), axis=1)

num_nan = 0
n_frames = []
print(len(frame))
for month in [1,3,4,5,6,7,9,10]:
    day_max = 31
    if month in [4, 6, 9]:
        day_max -=1
    print(month, day_max)
    for day in range(1, day_max+1):
        for hour in range(24):
            for loc_id in range(1,34):
                if len(frame[(frame["day"]==day)&(frame["month"]==month)&(frame["hour"]==hour)&(frame["loc_id"]==loc_id)]) == 0:
                    date_time = datetime.datetime(2017,month,day,hour,0,0)
                    time_stamp = date_time.strftime("%Y-%m-%d %H")
                    num_of_people = frame[(frame["week_day"]==date_time.weekday())&(frame["month"]==month)&(frame["hour"]==hour)&(frame["loc_id"]==loc_id)]["num_of_people"].mean()
                    if num_of_people is not np.nan:
                        n_frames.append([loc_id,time_stamp, num_of_people,date_time, month,day, hour, day//7, date_time.weekday()])
                        num_nan+=1

n_f = pd.DataFrame(n_frames,columns=frame.columns)
print(n_f.shape)
frame = pd.concat([frame, n_f], ignore_index=True).sort_values(by=["month","day","hour","loc_id"])
print(frame.shape)

num_nan2 = 0
# 处理假期值
for i in range(len(frame)):
    loc_id = frame.loc[i,"loc_id"]
    loc = location.check_loc(loc_id)
    day_type = check_day.check_day(frame.loc[i,"datetime"].date())
    if day_type == 3: # 长假
        if loc in [1, 2, 4]:
            week_day = frame.loc[i, "week_day"]
            month = frame.loc[i, "month"]
            hour = frame.loc[i, "hour"]
            v = frame[(frame["week_day"]==week_day)&(frame["month"]==month)&(frame["hour"]==hour)&(frame["loc_id"]==loc_id)]["num_of_people"].mean()
            if v is not np.nan:
                frame.loc[i, "num_of_people"] = v
                num_nan2 +=1
            
    if day_type == 2:
        week_day = frame.loc[i, "week_day"]
        month = frame.loc[i, "month"]
        hour = frame.loc[i, "hour"]
        v = frame[(frame["week_day"]==week_day)&(frame["month"]==month)&(frame["hour"]==hour)&(frame["loc_id"]==loc_id)]["num_of_people"].mean()
        if v is not np.nan:
            frame.loc[i, "num_of_people"] = v
            num_nan2 +=1
print(frame.shape)
frame = frame.sort_values(by=["month","day","hour","loc_id"])
frame.to_csv("/home/tanyx/dataDemo/campus2018/holiday_fix_diff1_10.csv",index=False, encoding="utf-8")

# 单独提取假期，计算假期权重
holidays = []
for i in range(len(frame)):
    if check_day.check_day(frame.loc[i, "datetime"].date()) == 2:
        holidays.append(frame.loc[i,:])
holiday_frame = pd.DataFrame(holidays, columns=frame.columns).sort_values(["month", "day", "hour", "loc_id"])
weight = {}
for i in [1,3,4,5,6,7,9,10,11]:
    weight[i] = {}
    for hour in range(24):
        weight[i][hour] = [1 for i in range(34)]
        for loc_id in range(1,34):
            holiday_value = holiday_frame[(holiday_frame["month"]==i)&(holiday_frame["hour"]==hour)&(holiday_frame["loc_id"]==loc_id)]["num_of_people"].mean()
            all_value = frame[(frame["month"]==i)&(frame["hour"]==hour)&(frame["loc_id"]==loc_id)]["num_of_people"].mean()
            weight[i][hour][loc_id] = holiday_value / all_value
weight_list = []
for month, value in weight.items():
    for hour, loc_ids in value.items():
        for loc_id in range(1,34):
            w = loc_ids[loc_id]
            weight_list.append([month, hour, loc_id, w])
weight_frame = pd.DataFrame(weight_list, columns=["month","hour","loc_id","weight"])
weight_frame.to_csv("/home/tanyx/dataDemo/campus2018/holiday_weight.csv", index=False)

raw11 = pd.read_csv("/home/tanyx/dataDemo/campus2018/11.csv")
data = {}
for i in range(len(raw11)):
    time_stamp = raw11.loc[i,"time_stamp"]
    loc_id = int(raw11.loc[i, "loc_id"])
    if time_stamp not in data:
        data[time_stamp] = [ 0 for i in range(34)]
    data[time_stamp][loc_id] += 1
f_list = []
for k, loc_ids in data.items():
    date_time = datetime.datetime.strptime(k, "%Y-%m-%d %H")
    for i in range(1,34):
        if loc_ids[i] > 0:
            f_list.append([i, k, loc_ids[i], date_time, date_time.month, date_time.day, date_time.hour, date_time.day//7, date_time.weekday()])
frame = pd.DataFrame(f_list, columns=["loc_id", "time_stamp", "num_of_people", "datetime", "month", "day", "hour", "week", "week_day"]).sort_values(by=["day", "hour", "loc_id"])
# 处理缺失值
num_nan = 0
n_frames = []
print(len(frame))
for day in range(1, 31):
    for hour in range(24):
        for loc_id in range(1,34):
            if len(frame[(frame["day"]==day)&(frame["hour"]==hour)&(frame["loc_id"]==loc_id)]) == 0:
                date_time = datetime.datetime(2017,11,day,hour,0,0)
                time_stamp = date_time.strftime("%Y-%m-%d %H")
                num_of_people = frame[(frame["week_day"]==date_time.weekday())&(frame["hour"]==hour)&(frame["loc_id"]==loc_id)]["num_of_people"].mean()
                if num_of_people is not np.nan:
                    n_frames.append([loc_id,time_stamp, num_of_people,date_time, 11,day, hour, day//7, date_time.weekday()])
                    num_nan+=1
n_f = pd.DataFrame(n_frames,columns=frame.columns)
print(n_f.shape)
frame = pd.concat([frame, n_f], ignore_index=True).sort_values(by=["month","day","hour","loc_id"])
print(frame.shape)
frame.to_csv("/home/tanyx/dataDemo/campus2018/holiday_fix_diff11.csv", index=False)

frame1_10 = pd.read_csv("/home/tanyx/dataDemo/campus2018/holiday_fix_diff1_10.csv")
frame_all = pd.concat([frame,frame1_10], ignore_index=True).sort_values(by=["month","day","hour","loc_id"])
frame_all.to_csv("/home/tanyx/dataDemo/campus2018/holiday_fix_diff_all.csv", index=False)
