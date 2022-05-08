#! -*- utf-8 -*-

import datetime
import re
from itertools import chain
import pymysql
from queue import Queue
import threading
import time

import retrying
from lxml import etree

# selenium 3.12.0
from selenium.webdriver import PhantomJS
import sys
import timeout_decorator

def use_selenium_headless_getdt(url):
    # ch_options = PhantomJS("C:\\Python310\\Scripts\\phantomjs.exe") # windows
    ch_options = PhantomJS() #linux
    ch_options.get(url)
    currentPageUrl = ch_options.current_url
    html = ch_options.page_source
    ch_options.close()
    return html,currentPageUrl


def get_FCPO_dt_fromDF():
    url ="http://quote.eastmoney.com/center/gridlist2.html#futures_110_1"
    html = use_selenium_headless_getdt(url)
    patt=re.compile('<a href="//quote.eastmoney.com/unify/r/110.MPM00Y">棕榈油当月连续</a></td><td class=".*?"><span class=".*?">(.*?)</span></td>',re.S)
    items = re.findall(patt,str(html))
    return items
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

        html,currentPageUrl= use_selenium_headless_getdt(url)
        patt = re.compile('<span class="text-2xl" data-test="instrument-price-last">(.*?)</span>',re.S)
        last_price = re.findall(patt,html)
        code_ = [currentPageUrl.split("/")[-1]]
        print(code_,last_price)
        print(currentPageUrl)
        dt_dict = {}
        print(url)
        dt_dict[code_[0]] = last_price[0]
        print(dt_dict)
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




def remove_dot(*args):
    big_list =[]
    for item in args:
        item = "".join(item.split(","))
        big_list.append(item)
    return big_list

def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='Futures',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    try:
        f_ls = "%s," * (8)
        print(len(f_ls[:-1].split(",")))
        cursor.executemany('insert into GF_Futures (ZS, ZC, ZL, ZM , ZW, HG, SB, CT) values ({0})'.format(f_ls[:-1]),content)
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

#@timeout_decorator.timeout(30)
def collection_func():

    sst = ZG_Futures()
    sst.run()
    e = datetime.datetime.now()
    f = e - s
    print(final_dt)


    # 异步之后还要排序
    f_tuple = tuple([list_dict(final_dt)[x] for x in global_futurescode])
    f_tuple = tuple(["".join(x.split(",")) for x in f_tuple])
    print(f_tuple)
    # 每10秒插入一次
    insertDB([f_tuple])
    print(final_dt)
    print(f)


if __name__=="__main__":
    while True:

        s = datetime.datetime.now()

        final_dt = []
        # 制只锁定在 10个左右 # 内存太小了，所以这次先缩减在6-7
        global_futurescode = ["us-soybeans", "us-corn", "us-soybean-oil", "us-soybean-meal", "us-wheat", "copper", "us-sugar-no11", "us-cotton-no.2"]
        url_list = ["https://cn.investing.com/commodities/{0}".format(x) for x in global_futurescode]
        collection_func()









# ZS, ZC, ZL, ZM , ZW, HG, SB, CT

# create table GF_Futures (id int not null primary key auto_increment,ZS TEXT, ZC TEXT, ZL TEXT, ZM TEXT, ZW TEXT, HG TEXT, SB TEXT, CT TEXT, LastTime timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP) engine=InnoDB  charset=utf8;




# drop table ZN_Futures;

# select * from GF_Futures;

# python接口说明   https://www.wenhua.com.cn/guide/jksm.htm

# Funcat 将同花顺、通达信、文华财经等的公式移植到了 Python 中。

# <a href="//quote.eastmoney.com/unify/r/110.MPM00Y">棕榈油当月连续</a></td><td class=".*?"><span class=".*?">(.*?)</span></td>