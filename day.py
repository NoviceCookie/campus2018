# -*- coding:utf-8 -*-
import datetime


class Day(object):
    def __init__(self):
        self.holidays = [
            datetime.date(2017, 1, 1),
            datetime.date(2017, 1, 2),
            datetime.date(2017, 4, 2),
            datetime.date(2017, 4, 3),
            datetime.date(2017, 4, 4),
            datetime.date(2017, 4, 29),
            datetime.date(2017, 4, 30),
            datetime.date(2017, 5, 1),
            datetime.date(2017, 5, 28),
            datetime.date(2017, 5, 29),
            datetime.date(2017, 5, 30),
            datetime.date(2017, 10, 1),
            datetime.date(2017, 10, 2),
            datetime.date(2017, 10, 3),
            datetime.date(2017, 10, 4),
            datetime.date(2017, 10, 5),
            datetime.date(2017, 10, 6),
            datetime.date(2017, 10, 7),
            datetime.date(2017, 10, 8),
            datetime.date(2017, 12, 30),
            datetime.date(2017, 12, 31)
        ]
        self.winter_vocation = (datetime.date(2017, 1, 21),
                                datetime.date(2017, 2, 25))
        self.summer_vocation = (datetime.date(2017, 7, 15),
                                datetime.date(2017, 8, 29))
        self.still_working = [
            datetime.date(2017, 4, 1),
            datetime.date(2017, 5, 27),
            datetime.date(2017, 9, 30)
        ]

    def check_day(self, day):
        if (self.winter_vocation[0] < day < self.winter_vocation[1]) or (self.summer_vocation[0] < day < self.summer_vocation[1]):
            return 3  # 长假
        if day in self.holidays:
            return 2  # 短假
        if (day.weekday() > 4) and (day not in self.still_working):
            return 1  # 周末
        return 0  # 工作
