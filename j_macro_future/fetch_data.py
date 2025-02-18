#! -*- coding:utf-8 -*-

# 2024.8.3

# 近一个月，日经回调明显，日银加息，重新把目光拉回交易市场，
# 期权以小博大的优势还是很明显，另外是否有套利的可能？ 所以现在想每天重新收集期权的数据
# 然后再做一个对比，每个月多一个20也是不错的，哪怕只有10 也是可以，这个也只有数据积累到一定数量
# 想法才能真出现
# 数据源1： https://svc.qri.jp/jpx/nkopm/1
# 数据源2：https://fu.minkabu.jp/chart/nk225_option

# 因为要统计最高，最低，同时作图，所以优先第二个数据源，整理好，直接用pandas插入数据库
# 积累到一定阶段之后就 用mplfinance 作图进行分析

import requests
from bs4 import BeautifulSoup
from datetime import datetime

import datetime
import time

import pymysql
import requests
from lxml import etree
from selenium import webdriver



from tqdm import tqdm
import time

# # 使用tqdm展示进度条
# for i in tqdm(range(1, 1200)):
#     # 模拟一些处理时间
#     time.sleep(0.01)

#
import uuid

class BS4Parse():
    def __init__(self, html_doc):
        self.soup = BeautifulSoup(html_doc, 'html.parser')

    def parseOneElement(self, tagName):
        trans_list = []
        for single_tag in self.soup.select(tagName):
            trans_list.append(" ".join(single_tag.text.split()))
        tagText = " ".join(trans_list)
        return tagText, trans_list
    def parseClassAttribute(self,outsidetag,classAttribute):
        trans_list = []
        ret = self.soup.findAll(name=outsidetag, attrs={"class":classAttribute})

        for item in ret:
            trans_list.append("".join(item.text))
        tagText = " ".join(trans_list)
        return tagText, trans_list


    def parseIDAttribute(self,DAttribute):
        trans_list = []
        ret = self.soup.findAll(id=DAttribute)

        for item in ret:
            trans_list.append("".join(item.text))
        tagText = " ".join(trans_list)
        return tagText, trans_list


    def fetchAllText(self):
        AllText = "".join(self.soup.get_text().split())
        return AllText


def generate_unique_id():
    unique_id = str(uuid.uuid4())[:8].lower()
    return unique_id


driver = webdriver.Chrome()
# 把find_elements 改为　find_element
def fetch_data(url):


    driver.get(url)
    time.sleep(2)
    html = driver.page_source
    return html




def to_integer(string):
    if "," in string:
        ret = "".join(string.split(","))

    else:
        ret = string

    if string=="":
        ret = "0"

    return ret



def today_string():
    # 获取当前日期
    current_date = datetime.datetime.now()
    # 格式化日期
    formatted_date = current_date.strftime('%Y-%m-%d')
    return formatted_date


def insert_into_DB(dbname,tbname,dt_tuple_list):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db=dbname,
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    cursor = connection.cursor()
    try:
        cursor.executemany('insert into {0} (strike_price,call_volume,call_close_p,call_low_p,call_high_p,call_open_p,put_volume,put_close_p,put_low_p,put_high_p,put_open_p,today_string) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'.format(tbname), dt_tuple_list)
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except TypeError:
        pass
    
    
    
# # Mplfinace 包可用于绘制任何数据帧，前提是满足以下条件
# # 
# # 日期是数据框的索引，日期采用 pd.datetime 格式。
# # Open: 开盘价
# # High: 期间最高价
# # Low : 期间最低价
# # Close : 收盘价
# # Volume : 期间交易量

if __name__ == '__main__':
    url = 'https://fu.minkabu.jp/chart/nk225_option'
    html_doc = fetch_data(url)

    element = etree.HTML(html_doc)

    call_volume = element.xpath('//*[@id="option_chart_table"]/table/tbody/tr/td[1]/text()')
    call_low_p = element.xpath('//*[@id="option_chart_table"]/table/tbody/tr/td[2]/text()')
    call_high_p = element.xpath('//*[@id="option_chart_table"]/table/tbody/tr/td[3]/text()')

    call_close_p = element.xpath('//*[@id="option_chart_table"]/table/tbody//td[4]/span[1]/text()')

    strike_price = element.xpath('//*[@id="option_chart_table"]/table/tbody/tr/td[5]/text()')

    put_close_p = element.xpath('//*[@id="option_chart_table"]/table/tbody//td[6]/span[1]/text()')

    put_changed_p = element.xpath('//*[@id="option_chart_table"]/table/tbody//td[6]/span[2]/text()')
    call_changed_p = element.xpath('//*[@id="option_chart_table"]/table/tbody//td[4]/span[2]/text()')

    put_high_p = element.xpath('//*[@id="option_chart_table"]/table/tbody//td[7]/text()')
    put_low_p = element.xpath('//*[@id="option_chart_table"]/table/tbody//td[8]/text()')
    put_volume = element.xpath('//*[@id="option_chart_table"]/table/tbody//td[9]/text()')


    today_string = today_string()
    put_open_p = ""
    call_open_p = ""
    for i1,i2,i3,i4,i5,i6,i7,i8,i9,i10,i11 in zip(strike_price,call_volume,call_close_p,call_low_p,call_high_p,call_changed_p,put_volume,put_close_p,put_low_p,put_high_p,put_changed_p):
        # call : i3 i4,i5,i6
        # put:  i8,i9,i10,i11
        modified_list1 = [item if item != "-" else "" for item in [i1,i2,i3,i4,i5,i6,i7,i8,i9,i10,i11,today_string]]
        # modified_list2 = [item if item != "" else 0 for item in modified_list1]
        integer_list = [to_integer(x) for x in modified_list1]

        # call的現價更換
        call_open_p = int(integer_list[2]) - int(integer_list[5])
        integer_list[5] = str(call_open_p)


        # put的現價更換

        put_open_p = int(integer_list[7]) - int(integer_list[10])
        integer_list[10] = str(put_open_p)
        #
        print(integer_list)
        time.sleep(0.1)
        insert_into_DB("jp_invest","nikkei_opt_data",[(tuple(integer_list))])



# strike_price,call_volume,call_close_p,call_low_p,call_high_p,call_open_p,put_volume,put_close_p,put_low_p,put_high_p,put_open_p
# create table nikkei_opt_data(
# id int not null primary key auto_increment,
# strike_price varchar(20),
# call_volume varchar(20),
# call_close_p varchar(20),
# call_low_p varchar(20),
# call_high_p varchar(20),
# call_open_p varchar(20),
# put_volume varchar(20),
# put_close_p varchar(20),
# put_low_p varchar(20),
# put_high_p varchar(20),
# put_open_p varchar(20),
# today_string varchar(20)
# ) engine=InnoDB default charset=utf8;



#  drop table nikkei_opt_data;