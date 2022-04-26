




import os
import sys
import time
import datetime
s = datetime.datetime.now()
import subprocess

def use_subprocess_command(command_string):


    process = subprocess.Popen(command_string, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    process.wait()
    command_output = process.stdout.read().decode('utf-8')
    # command_output:str
    return command_output

if __name__=="__main__":
    while True:
        time.sleep(0.1)
        use_subprocess_command("python3 Daily_fetch_dt_YC.py")
        time.sleep(0.1)
        e = datetime.datetime.now()
        print(e)
        f = e - s
        print(f)


# 放弃计划任务,还是跟服务器性能有关

# 明天进行计算的思考 ，划分！


#1.自己，模拟对照mt5的模型还是很有必要的。这就是我手动做的辅助线

# 2.时间采集是没有问题了
# 3 明天就把日内波动的参数给整理出来
#4. 目前就解决两个额问题 ，就是 取30分钟和取3分钟的 。就是时间的选取函数
# 5. 30分钟计算，  3分钟计算 ，同时 信号和验证都放在一起

# 8个做到隔离！


# create table ZN_Futures (id int not null primary key auto_increment,ym TEXT,vm TEXT,TAM TEXT,rbm TEXT,pm TEXT,OIM TEXT,mm TEXT,MAM TEXT,lm TEXT,im TEXT,FGM TEXT,bum TEXT,APM TEXT,LastTime timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP) engine=InnoDB  charset=utf8;




# drop table ZN_Futures;

# select * from ZN_Futures;