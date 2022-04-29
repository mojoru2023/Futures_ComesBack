import itertools
import sys
import html
from logging import Formatter, handlers, StreamHandler, getLogger, DEBUG
import csv
import os
import time
import copy
import re
import datetime
from itertools import chain
import pymysql
from queue import Queue
import threading
from func_timeout import func_set_timeout
from lxml import etree
import func_timeout
# selenium 3.12.0
from selenium.webdriver import PhantomJS


def run_forever(func):
    def wrapper(obj):
        while True:
            func(obj)
    return wrapper


class ZG_Futures(object):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
        }
        self.url_pattern = '{0}'
        # url 队列
        self.url_queue = Queue()


    def add_url_to_queue(self):
        for i in url_list:
            print(i)

            self.url_queue.put(self.url_pattern.format(i))


    @run_forever
    def add_page_to_queue(self):
        ''' 发送请求获取数据 '''
        url = self.url_queue.get()

        html= use_selenium_headless_getdt(url)
        selector = etree.HTML(html)
        last_price = selector.xpath('//*[@id="datas2"]/text()')
        code_ = selector.xpath('//*[@id="datas1"]/text()')

        for i1,i2 in zip(code_,last_price):
            dt_dict = {}
            if i1 in forSort_futurescode:
                dt_dict[i1] = i2
                final_dt.append(dt_dict)




        # 完成当前URL任务
        self.url_queue.task_done()




    def run_use_more_task(self,func,count=1):
        for i in range(0,count):
            t = threading.Thread(target=func)
            t.setDaemon(True)
            t.start()
    def run(self):
        url_t = threading.Thread(target=self.add_url_to_queue)
        url_t.setDaemon(True)
        url_t.start()

        self.run_use_more_task(self.add_page_to_queue,4)
         # 使用队列join方法,等待队列任务都完成了才结束
        self.url_queue.join()









def use_selenium_headless_getdt(url):
    #ch_options = PhantomJS("D:\\python3.10\\Scripts\\phantomjs.exe") # windows
    ch_options = PhantomJS() #linux
    ch_options.get(url)
    html = ch_options.page_source
    ch_options.close()
    return html



def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='Futures',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    try:
        f_ls = "%s," * (13)
        print(len(f_ls[:-1].split(",")))
        cursor.executemany('insert into ZN_Futures (ym,vm,TAM,rbm,pm,OIM,mm,MAM,lm,im,FGM,bum,APM) values ({0})'.format(f_ls[:-1]),content)
        connection.commit()
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except TypeError:
        pass
#合并list的字典
def list_dict(list_data):
    dict_data = {}
    for i in list_data:
        key, = i
        value, = i.values()
        dict_data[key] = value
    return dict_data


def is_need_retry(exception:Exception)->bool:
    return isinstance(exception,func_timeout.exceptions.FunctionTimedOut)
import timeout_decorator
@timeout_decorator.timeout(20)
def collection_func():
    sst = ZG_Futures()
    sst.run()
    e = datetime.datetime.now()
    f = e - s
    print(final_dt)
    # [{'rbm': '4960'}, {'TAM': '6182'}, {'im': '875.5'}, {'ppm': '8697'}, {'jmm': '3003.0'}, {'pm': '11470'}, {'mm': '4062'}, {'jm': '3799.5'}]

    # 异步之后还要排序
    f_tuple = tuple([list_dict(final_dt)[x] for x in forSort_futurescode])
    print(f_tuple)
    # 每10秒插入一次
    insertDB([f_tuple])
    print(final_dt)
    print(f)
    sys.exit(0)

if __name__=="__main__":
    s = datetime.datetime.now()

    final_dt =[]
    #制只锁定在 10个左右 # 内存太小了，所以这次先缩减在6-7
    forSort_futurescode =["豆油主力","PVC主力","PTA主力","螺纹钢主力","棕榈油主力","菜籽油主力","豆粕主力","甲醇主力","聚乙烯主力","铁矿石主力","玻璃主力","沥青主力","苹果主力"]
    url_list = ["http://www.ucai123.com/datas-zgqhhq"]
    collection_func()








# create table ZN_Futures (id int not null primary key auto_increment,ym TEXT,vm TEXT,TAM TEXT,rbm TEXT,pm TEXT,OIM TEXT,mm TEXT,MAM TEXT,lm TEXT,im TEXT,FGM TEXT,bum TEXT,APM TEXT,LastTime timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP) engine=InnoDB  charset=utf8;

# python接口说明   https://www.wenhua.com.cn/guide/jksm.htm

# Funcat 将同花顺、通达信、文华财经等的公式移植到了 Python 中。


# drop table ZN_Futures;