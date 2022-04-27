
import os
import sys
import time
import datetime

import subprocess









import time
import random
from datetime import datetime
import os

import csv
# 先识别本地是否有文件
# 无文件,进行信号甄别;有文件,就验证信号
# 先送30分钟的数据
# 信号确认 有信号,无信号
# 有信号时创建文件,退出
# 下次进场,有文件,读取文件信息,结合当次数据发送信号确认的情况。
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



def writeintotxt_file(filename,data):
    with open(filename,'a', newline='\n', encoding="utf-8") as f_output:
        tsv_output = csv.writer(f_output, delimiter=',')
        tsv_output.writerow(data)
writeintotxt_file("put.txt",["put",-5])
writeintotxt_file("put.txt",["call",66])

def readDatafile(filename):
    line_list = []
    call_list = []
    put_list = []
    with open(filename,"r", encoding="utf-8") as f:
        for line in f.readlines():
            line = line.strip("\n")
            line_list.append(line)
    for item in line_list:
        if "put" in item:
            put_list.append(float(item.split(",")[1]))
        elif "call" in item:
            call_list.append(float(item.split(",")[1]))
    total_list = sum(call_list)+sum(put_list)

    return sum(call_list),sum(put_list),total_list



def remove_existfile(filename):
    if os.path.exists(filename):
        os.remove(filename)
def remove_file(filetype):
    for file in os.listdir("."):
        file_list = file.split(".")
        if len(file_list) != 1:
            if file.split(".")[1] == filetype:
                os.remove(file)
def find_and_confirm_signal(tradeone,base_dt,base_dt_minus3,base_dt_minus30,trade_dict,find_param,confirm_param):


    # 识别信号
    if os.path.exists('call{0}.txt'.format(tradeone)) is False and os.path.exists('put{0}.txt'.format(tradeone)) is False:
        # 无文件,进行信号甄别;有文件,就验证信号
        find_signal_dt = base_dt-base_dt_minus30
        find_signal_msg = "tradeone is {2} \n time: {1} \n 市场为 {0} ，发现信号！".format(str(find_signal_dt),datetime.now().strftime("%Y-%m-%d %H:%M:%S"),tradeone)
        if find_signal_dt>trade_dict[tradeone]*find_param:
            print(find_signal_msg)
            open('call{0}.txt'.format(tradeone), mode='w')
        elif find_signal_dt < -trade_dict[tradeone]*find_param:
            print(find_signal_msg)
            open('put{0}.txt'.format(tradeone), mode='w')
        else:
            pass

    else: #验证信号
        if os.path.exists('call{0}.txt'.format(tradeone)) is True:
            confirm_signal_dt = base_dt-base_dt_minus3
            if confirm_signal_dt>0:
                # 写入文件
                writeintotxt_file("call{0}.txt", ["call",confirm_signal_dt])
                # 读取文件
                call_list, put_list, total_list = readDatafile("call{0}.txt")
                msg1 = "本次判定信号是正确的！ 市场为 {0} ，考虑是否进场！".format(str(confirm_signal_dt))
                msg2 = "判定信号 正确的数值为{0} ！".format(str(call_list))
                msg3 = "判定信号 错误的数值为{0} ！".format(str(put_list))
                msg4 = "判定信号 总计的数值为{0} ！".format(str(total_list))
                print(msg1)
                print(msg2)
                print(msg3)
                print(msg4)
                if abs(put_list)-abs(call_list) >trade_dict[tradeone]*confirm_param:
                    msg5 = "做多的信号彻底失败！赶紧离场！"
                    print(msg5)
                    remove_existfile("call{0}.txt")
            elif confirm_signal_dt<0:
                # 写入文件
                writeintotxt_file("call{0}.txt", ["put",confirm_signal_dt])
                # 读取文件
                call_list, put_list, total_list = readDatafile("call{0}.txt")
                # 1. 本次判定的信号的结果 ，和
                # 2. 累积判定正确的信号的结果 ，和
                # 3. 累积判定错误的信号的结果 ，和
                # 4. 累积判定的信号的结果 ，和
                # 5. 合计的 加上40点 还是为负说明信号彻底失效！ 删除txt文件

                msg1 = "本次判定信号是正确的！ 市场为 {0} ，考虑是否进场！".format(str(confirm_signal_dt))
                msg2 = "判定信号 正确的数值为{0} ！".format(str(call_list))
                msg3 = "判定信号 错误的数值为{0} ！".format(str(put_list))
                msg4 = "判定信号 总计的数值为{0} ！".format(str(total_list))
                print(msg1)
                print(msg2)
                print(msg3)
                print(msg4)
                if abs(put_list)-abs(call_list) >trade_dict[tradeone]*confirm_param:
                    msg5 = "做多的信号彻底失败！赶紧离场！"
                    print(msg5)
                    remove_existfile("call{0}.txt")



        # 读取文件信息,结合当次数据发送信号确认的情况。
        elif os.path.exists('put{0}.txt'.format(tradeone)) is True:
            confirm_signal_dt = base_dt-base_dt_minus3
            if confirm_signal_dt>0:
                # 写入文件
                writeintotxt_file("put{0}.txt", ["call",confirm_signal_dt])
                # 读取文件
                call_list, put_list, total_list = readDatafile("put{0}.txt")
                # 1. 本次判定的信号的结果 ，和
                # 2. 累积判定正确的信号的结果 ，和
                # 3. 累积判定错误的信号的结果 ，和
                # 4. 累积判定的信号的结果 ，和
                # 5. 合计的 加上40点 还是为负说明信号彻底失效！ 删除txt文件

                msg1 = "本次判定信号是正确的！ 市场为 {0} ，考虑是否进场！".format(str(confirm_signal_dt))
                msg2 = "判定信号 正确的数值为{0} ！".format(str(put_list))
                msg3 = "判定信号 错误的数值为{0} ！".format(str(call_list))
                msg4 = "判定信号 总计的数值为{0} ！".format(str(total_list))
                print(msg1)
                print(msg2)
                print(msg3)
                print(msg4)
                if abs(call_list)-abs(put_list) >trade_dict[tradeone]*confirm_param:
                    msg5 = "做空的信号彻底失败！赶紧离场！"
                    print(msg5)
                    remove_existfile("put{0}.txt")
            elif confirm_signal_dt<0:
                # 写入文件
                writeintotxt_file("put{0}.txt", ["put",confirm_signal_dt])
                # 读取文件
                call_list, put_list, total_list = readDatafile("put{0}.txt")
                # 1. 本次判定的信号的结果 ，和
                # 2. 累积判定正确的信号的结果 ，和
                # 3. 累积判定错误的信号的结果 ，和
                # 4. 累积判定的信号的结果 ，和
                # 5. 合计的 加上40点 还是为负说明信号彻底失效！ 删除txt文件

                msg1 = "本次判定信号是正确的！ 市场为 {0} ，考虑是否进场！".format(str(confirm_signal_dt))
                msg2 = "判定信号 正确的数值为{0} ！".format(str(put_list))
                msg3 = "判定信号 错误的数值为{0} ！".format(str(call_list))
                msg4 = "判定信号 总计的数值为{0} ！".format(str(total_list))
                print(msg1)
                print(msg2)
                print(msg3)
                print(msg4)
                if abs(call_list)-abs(put_list) >trade_dict[tradeone]*confirm_param:
                    msg5 = "做空的信号彻底失败！赶紧离场！"
                    print(msg5)
                    remove_existfile("put{0}.txt")



def use_subprocess_command(command_string):


    process = subprocess.Popen(command_string, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    process.wait()
    command_output = process.stdout.read().decode('utf-8')
    # command_output:str
    return command_output



if __name__=="__main__":
    # 开始时, 删除所有文本
    remove_file("txt")
    trade_base_params_dict = {'ym': 106.43, 'vm': 125.85, 'TAM': 117, 'rbm': 70.31, 'pm': 122.95, 'OIM': 131.77,
                              'mm': 36.1, 'MAM': 31.176, 'lm': 197.95, 'im': 45.46, 'FGM': 101.4, 'bum': 62.533,
                              'APM': 117.53}
    while True:
        e = datetime.datetime.now()
        print(e)
        base_dt,base_dt_minus3_dt,base_dt_minus20_dt = fetch_basedt_minus3dt_minus20dt()
        print(base_dt)
        print(base_dt_minus3_dt)
        print(base_dt_minus20_dt)
        find_and_confirm_signal("ym",base_dt,base_dt_minus3_dt,base_dt_minus20_dt,trade_base_params_dict,0.22,0.13)
        find_and_confirm_signal("vm",base_dt,base_dt_minus3_dt,base_dt_minus20_dt,trade_base_params_dict,0.22,0.13)
        find_and_confirm_signal("TAM",base_dt,base_dt_minus3_dt,base_dt_minus20_dt,trade_base_params_dict,0.22,0.13)
        find_and_confirm_signal("rbm",base_dt,base_dt_minus3_dt,base_dt_minus20_dt,trade_base_params_dict,0.22,0.13)
        find_and_confirm_signal("pm",base_dt,base_dt_minus3_dt,base_dt_minus20_dt,trade_base_params_dict,0.22,0.13)
        find_and_confirm_signal("OIM",base_dt,base_dt_minus3_dt,base_dt_minus20_dt,trade_base_params_dict,0.22,0.13)
        find_and_confirm_signal("mm",base_dt,base_dt_minus3_dt,base_dt_minus20_dt,trade_base_params_dict,0.22,0.13)
        find_and_confirm_signal("MAM",base_dt,base_dt_minus3_dt,base_dt_minus20_dt,trade_base_params_dict,0.22,0.13)
        find_and_confirm_signal("lm",base_dt,base_dt_minus3_dt,base_dt_minus20_dt,trade_base_params_dict,0.22,0.13)
        find_and_confirm_signal("im",base_dt,base_dt_minus3_dt,base_dt_minus20_dt,trade_base_params_dict,0.22,0.13)
        find_and_confirm_signal("FGM",base_dt,base_dt_minus3_dt,base_dt_minus20_dt,trade_base_params_dict,0.22,0.13)
        find_and_confirm_signal("bum",base_dt,base_dt_minus3_dt,base_dt_minus20_dt,trade_base_params_dict,0.22,0.13)
        find_and_confirm_signal("APM",base_dt,base_dt_minus3_dt,base_dt_minus20_dt,trade_base_params_dict,0.22,0.13)
        time.sleep(5)












# select * from ZN_Futures  order by id desc limit 10;
