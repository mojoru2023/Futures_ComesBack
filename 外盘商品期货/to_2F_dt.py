




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
        use_subprocess_command("python3 F_Daily_fetch_dt_DF.py")
        time.sleep(2)


        e = datetime.datetime.now()
        print(e)
        f = e - s
        print(f)


