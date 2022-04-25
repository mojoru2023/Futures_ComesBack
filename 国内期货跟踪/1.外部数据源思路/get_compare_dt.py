

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
    final_result =None
    df_result = base_df[(base_df[one_params] >= df1_time) & (base_df[one_params] <= df2_time)]
    result_list = df_result.values.tolist()
    random_list_result1 = random.choice(result_list)[1:-1]
    random_list_result2 = random.choice(result_list)[1:-1]
    random_list_result3 = random.choice(result_list)[1:-1]
    if "--" not in random_list_result1:
        final_result = random_list_result1
    elif "--" not in random_list_result2:
        final_result = random_list_result2
    elif "--" not in random_list_result3:
        final_result = random_list_result3
    return final_result
def minum_basetime_minus_N_minutes(string_datetime, N_minutes):
    string_datetime = datetime.datetime.strptime(string_datetime, "%Y-%m-%d %H:%M:%S")  # 把strTime转化为时间格式,后面的秒位自动补位的
    minum_basetime_minusN = (string_datetime + datetime.timedelta(minutes=-N_minutes)).strftime("%Y-%m-%d %H:%M:%S")
    return minum_basetime_minusN

def fetch_basedt_minus3dt_minus30dt():

    engine_ZN_Futures = create_engine('mysql+pymysql://root:123456@localhost:3306/Futures')
    # 逆序取数
    sql_ZN_Futures = 'select * from ZN_Futures  order by id desc ; '
    # 取第一行数
    df_ZN_Futures = pd.read_sql_query(sql_ZN_Futures, engine_ZN_Futures)
    # 取第一行数
    last_row = list(df_ZN_Futures.iloc[0])
    # remove id ,remove lasttime
    base_id = last_row[0]
    base_dt = last_row[1:-1]
    base_time_string = str(last_row[-1])
    result_dt = base_dt
    _base_time_minus3 = minum_basetime_minus_N_minutes(base_time_string,3)
    _base_time_minus4 = minum_basetime_minus_N_minutes(base_time_string,4)
    _base_time_minus29 = minum_basetime_minus_N_minutes(base_time_string,29)
    _base_time_minus30 = minum_basetime_minus_N_minutes(base_time_string,30)
    base_dt_minus3_dt = difference_set_fromTwo_df(df_ZN_Futures,"LastTime",_base_time_minus4,_base_time_minus3)
    base_dt_minus30_dt = difference_set_fromTwo_df(df_ZN_Futures,"LastTime",_base_time_minus30,_base_time_minus29)

    if "--" in base_dt:
        engine_ZN_Futures2 = create_engine('mysql+pymysql://root:123456@localhost:3306/Futures')
        # 逆序取数
        sql_ZN_Futures2 = 'select * from ZN_Futures where id ={0} ; '.format(base_id-1)
        # 取第一行数
        df_ZN_Futures2 = pd.read_sql_query(sql_ZN_Futures2, engine_ZN_Futures2)
        # 取第一行数
        last_row2 = list(df_ZN_Futures2.iloc[0])
        base_dt2 = last_row2[1:-1]
        result_dt = base_dt2


    #取范围内的3分钟,30分钟的数



    # minutes 3-4    minutes 29-30



    # 方向是一致的然后选取相同的部分dataframe



    return result_dt,base_dt_minus3_dt,base_dt_minus30_dt






base_dt,base_dt_minus3_dt,base_dt_minus30_dt = fetch_basedt_minus3dt_minus30dt()
print(base_dt,base_dt_minus3_dt,base_dt_minus30_dt)
