
# ! -*- coding:utf-8 -*-
# 增加index部位的手数
import time
import re
import pymysql
from lxml import etree
import time
import datetime
from math import floor

from selenium import webdriver



# 2019.6.30 开始统计美豆框架数据 跑个2年吧



def call_page(url):
    driver.get(url)
    html = driver.page_source
    return html

# 　选择依次请求５个股票和一个指数后再关闭浏览器




def parse_A_M_J_Spread():
    url_A = 'https://finance.sina.com.cn/futures/quotes/S.shtml'
    html = call_page(url_A)
    selector = etree.HTML(html)
    A_Value= selector.xpath('//*[@id="table-box-futures-hq"]/tbody/tr[1]/td[1]/div/span[1]/text()')
    for item in A_Value:
        big_list.append(item)


    url_M = 'https://finance.sina.com.cn/futures/quotes/SM.shtml'
    html = call_page(url_M)
    selector = etree.HTML(html)
    M_Value= selector.xpath('//*[@id="table-box-futures-hq"]/tbody/tr[1]/td[1]/div/span[1]/text()')
    for item in M_Value:
        big_list.append(item)



    url_Y = 'https://finance.sina.com.cn/futures/quotes/BO.shtml'
    html = call_page(url_Y)
    selector = etree.HTML(html)
    Y_Value= selector.xpath('//*[@id="table-box-futures-hq"]/tbody/tr[1]/td[1]/div/span[1]/text()')
    for item in Y_Value:
        big_list.append(item)



def float_2_str(item):
    f_item = float(item)
    ff_item = round(f_item,2)
    ff_str_item = str(ff_item)
    return ff_str_item







def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='Futures',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    try:
        cursor.executemany('insert into A_M_Y_Spread_USA (A_value,M_Value,Y_Value,A_Y_Spread,M_Y_Spread) values (%s,%s,%s,%s,%s)', content)
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except :
        print('出列啦')



if __name__ == '__main__':

    while True:
        driver = webdriver.Chrome()

        big_list = []
        time.sleep(15)

        parse_A_M_J_Spread()
        A = big_list[0]
        M = big_list[1]
        Y = big_list[2]
        f_A_Y_Spread = float(A) - float(Y)
        A_Y_Spread =  float_2_str(f_A_Y_Spread)

        f_M_Y_Spread = float(M) - float(Y)
        M_Y_Spread = float_2_str(f_M_Y_Spread)

        big_list.append(A_Y_Spread)
        big_list.append(M_Y_Spread)

        driver.quit()

        l_tuple = tuple(big_list)
        content = []
        content.append(l_tuple)
        insertDB(content)
        print(datetime.datetime.now())


#

# A_value,M_Value,Y_Value,A_Y_Spread,M_Y_Spread


# create table A_M_Y_Spread_USA(
# id int not null primary key auto_increment,
# A_value varchar(10),
# M_Value varchar(10),
# Y_Value varchar(10),
# A_Y_Spread varchar(10),
# M_Y_Spread varchar(10),
# LastTime timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
# ) engine=InnoDB  charset=utf8;


# drop  table M_Y_Spread_USA;