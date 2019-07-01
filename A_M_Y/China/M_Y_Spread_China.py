
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



# # 2019.6.30 开始统计内盘粕油数据  跑个2年吧



def call_page(url):
    driver.get(url)
    html = driver.page_source
    return html

# 　选择依次请求５个股票和一个指数后再关闭浏览器




def parse_M_J_Spread():
    url_M = 'http://quote.eastmoney.com/qihuo/MM.html'
    html = call_page(url_M)
    selector = etree.HTML(html)
    M_Value= selector.xpath('/html/body/div[1]/div[4]/div/div[1]/p[1]/i[1]/text()')
    for item in M_Value:
        big_list.append(item)


    url_Y = 'http://quote.eastmoney.com/qihuo/ym.html'
    html = call_page(url_Y)
    selector = etree.HTML(html)
    Y_Value= selector.xpath('/html/body/div[1]/div[4]/div/div[1]/p[1]/i[1]/text()')
    for item in Y_Value:
        big_list.append(item)












def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='Futures',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    try:
    # 这里是判断big_list的长度，不是content字符的长度
        cursor.executemany('insert into M_Y_Spread_China (M_Value,Y_Value,M_Y_Spread) values (%s,%s,%s)', content)
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except :
        print('出列啦')



def float_2_str(item):
    f_item = float(item)
    ff_item = round(f_item,2)
    ff_str_item = str(ff_item)
    return ff_str_item

if __name__ == '__main__':

    while True:
        driver = webdriver.Chrome()

        big_list = []
        time.sleep(5)

        parse_M_J_Spread()
        M = big_list[0]
        Y = big_list[1]
        f_M_Y_Spread = int(M) - int(Y)
        # 将计算结果取两位变成浮点数，同事再取两位数
        M_Y_Spread = float_2_str(f_M_Y_Spread)
        big_list.append(M_Y_Spread)

        driver.quit()

        l_tuple = tuple(big_list)
        content = []
        content.append(l_tuple)
        insertDB(content)
        print(datetime.datetime.now())


#

# M_Value,Y_Value,M_Y_Spread


# create table M_Y_Spread_China(
# id int not null primary key auto_increment,
# M_Value varchar(10),
# Y_Value varchar(10),
# M_Y_Spread varchar(10),
# LastTime timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
# ) engine=InnoDB  charset=utf8;


# drop  table M221_2A_Index;