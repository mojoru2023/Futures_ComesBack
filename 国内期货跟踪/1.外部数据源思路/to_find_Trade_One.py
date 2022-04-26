





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
trade_dict ={}



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

call_list,put_list,total_list =  readDatafile("put.txt")

print(call_list)
print(put_list)
print(total_list)
def remove_existfile(filename):
    if os.path.exists(filename):
        os.remove(filename)
def remove_file(filetype):
    for file in os.listdir("."):
        file_list = file.split(".")
        if len(file_list) != 1:
            if file.split(".")[1] == filetype:
                os.remove(file)
def find_and_confirm_signal(tradeone,base_dt,base_dt_minus3,base_dt_minus30):
    # 识别信号
    if os.path.exists('call{0}.txt'.format(tradeone)) is False and os.path.exists('put{0}.txt'.format(tradeone)) is False:
        # 无文件,进行信号甄别;有文件,就验证信号
        find_signal_dt = base_dt-base_dt_minus30
        find_signal_msg = "tradeone is {2} \n time: {1} \n 市场为 {0} ，发现信号！".format(str(find_signal_dt),datetime.now().strftime("%Y-%m-%d %H:%M:%S"),tradeone)
        if find_signal_dt>trade_dict[tradeone]*0.33:
            print(find_signal_msg)
            open('call{0}.txt'.format(tradeone), mode='w')
        elif find_signal_dt < -trade_dict[tradeone]*0.33:
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
                if abs(put_list)-abs(call_list) >trade_dict[tradeone]*0.15:
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
                if abs(put_list)-abs(call_list) >trade_dict[tradeone]*0.15:
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
                if abs(call_list)-abs(put_list) >trade_dict[tradeone]*0.15:
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
                if abs(call_list)-abs(put_list) >trade_dict[tradeone]*0.15:
                    msg5 = "做空的信号彻底失败！赶紧离场！"
                    print(msg5)
                    remove_existfile("put{0}.txt")


if __name__=="__main__":
    # 开始时, 删除所有文本
    remove_file("txt")

