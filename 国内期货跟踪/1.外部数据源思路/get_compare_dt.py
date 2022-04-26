

# !/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import datetime
import sys

import pymysql
import pandas as pd
import random
from sqlalchemy import create_engine
import pymysql
import pandas as pd
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import datetime


def difference_set_fromTwo_df(base_df, one_params, df1_time, df2_time):
    #  df1_time > df2_time
    df_result =base_df[(base_df[one_params] >= df1_time) & (base_df["LastTime"] <= df2_time)]
    result_list = df_result.values.tolist()
    final_result = random.choice(result_list)
    final_result_dt = final_result[1:-1]
    return final_result_dt

def minum_basetime_minus_N_minutes(string_datetime, N_minutes):
    string_datetime = datetime.datetime.strptime(string_datetime, "%Y-%m-%d %H:%M:%S")  # 把strTime转化为时间格式,后面的秒位自动补位的
    minum_basetime_minusN = (string_datetime + datetime.timedelta(minutes=-N_minutes)).strftime("%Y-%m-%d %H:%M:%S")
    return minum_basetime_minusN

def fetch_basedt_minus3dt_minus20dt():

    engine_ZN_Futures = create_engine('mysql+pymysql://root:123456@localhost:3306/Futures')
    # 逆序取数
    sql_ZN_Futures = 'select * from ZN_Futures  order by id desc ; '
    # 取第一行数
    df_ZN_Futures = pd.read_sql_query(sql_ZN_Futures, engine_ZN_Futures)
    # 取第一行数
    last_row = list(df_ZN_Futures.iloc[0])
    # remove id ,remove lasttime
    base_dt = last_row[1:-1]
    base_time_string = str(last_row[-1])

    _base_time_minus3 = minum_basetime_minus_N_minutes(base_time_string,3)
    _base_time_minus4 = minum_basetime_minus_N_minutes(base_time_string,4)
    _base_time_minus15 = minum_basetime_minus_N_minutes(base_time_string,15)
    _base_time_minus20 = minum_basetime_minus_N_minutes(base_time_string,20)
    base_dt_minus3_dt = difference_set_fromTwo_df(df_ZN_Futures,"LastTime",_base_time_minus4,_base_time_minus3)
    base_dt_minus20_dt = difference_set_fromTwo_df(df_ZN_Futures,"LastTime",_base_time_minus20,_base_time_minus15)
    return base_dt,base_dt_minus3_dt,base_dt_minus20_dt
# 数据收集还是





base_dt,base_dt_minus3_dt,base_dt_minus20_dt = fetch_basedt_minus3dt_minus20dt()
print(base_dt,base_dt_minus3_dt,base_dt_minus20_dt)
