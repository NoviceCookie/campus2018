# -*- coding:utf-8 -*-
import pandas as pd
import datetime
frame = pd.read_csv("/home/tanyx/dataDemo/campus2018/no_holiday_all.csv")


def get_data(frame, time_stamp, loc_id):
    week = time_stamp.day // 7
    week_day = time_stamp.weekday()
    hour = time_stamp.hour
    if week == 4:
        week = 3
    x = frame[(frame["week"] == week) & (frame["week_day"] == week_day) & (frame["hour"] == hour) & (frame["loc_id"] == loc_id)]
    return x.sort_values(by="month")["num_of_people"].values.tolist()


data = get_data(frame, datetime.datetime(2017, 11, 1, 2, 0, 0), 1)
print(data)
