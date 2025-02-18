import sqlite3
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from lxml import etree
from selenium import webdriver
import time
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

    def fetchAllText(self):
        AllText = "".join(self.soup.get_text().split())
        return AllText


def generate_unique_id():
    unique_id = str(uuid.uuid4())[:8].lower()
    return unique_id


driver = webdriver.Chrome()

def translate_date(date_string):
    # 原始日期字符串
    # 转换为 datetime 对象
    date_object = datetime.strptime(date_string, '%b %d %Y')

    # 将 datetime 对象格式化为 ISO 8601 格式（YYYY-MM-DD）
    formatted_date = date_object.strftime('%Y-%m-%d')
    return formatted_date # 输出: 2023-09-11


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

    if string == "":
        ret = "0"

    return ret




def insert_into_DB(dbname, tbname, dt_tuple_list):
    connection = sqlite3.connect(dbname)
    cursor = connection.cursor()

    # 创建表（如果不存在）
    cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS {tbname} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date_ TEXT UNIQUE,
        open_ TEXT,
        high_ TEXT,
        low_ TEXT,
        close_ TEXT,
        adj_close TEXT,
        volume_ TEXT
    )
    ''')

    try:
        for item in dt_tuple_list:
            date_value = item[0]

            # 查询日期是否已存在
            cursor.execute(f'SELECT COUNT(*) FROM {tbname} WHERE date_ = ?', (date_value,))
            exists = cursor.fetchone()[0] > 0

            if not exists:
                # 插入数据
                cursor.execute(
                    f'INSERT INTO {tbname} (date_, open_, high_, low_, close_, adj_close, volume_) VALUES (?, ?, ?, ?, ?, ?, ?)',
                    item
                )
                print(f'向SQLite中添加数据成功: {item}')
            else:
                print(f'日期 {date_value} 已存在，跳过插入。')

        connection.commit()
    except Exception as e:
        print(f"插入数据出错: {e}")
    finally:
        connection.close()



if __name__ == '__main__':
    dt_tuple_list = []
    # 数据库名称和表名
    db_name = 'us_invest.db'
    table_name = 'sp500_index'

    url = 'https://finance.yahoo.com/quote/%5EGSPC/history/'
    html_doc = fetch_data(url)

    element = etree.HTML(html_doc)

    date_ = element.xpath(
        '//*[@id="nimbus-app"]/section/section/section/article/div[1]/div[3]/table/tbody/tr/td[1]/text()')
    open_ = element.xpath(
        '//*[@id="nimbus-app"]/section/section/section/article/div[1]/div[3]/table/tbody/tr/td[2]/text()')
    high_ = element.xpath(
        '//*[@id="nimbus-app"]/section/section/section/article/div[1]/div[3]/table/tbody/tr/td[3]/text()')
    low_ = element.xpath(
        '//*[@id="nimbus-app"]/section/section/section/article/div[1]/div[3]/table/tbody/tr/td[4]/text()')
    close_ = element.xpath(
        '//*[@id="nimbus-app"]/section/section/section/article/div[1]/div[3]/table/tbody/tr/td[5]/text()')
    adj_close = element.xpath(
        '//*[@id="nimbus-app"]/section/section/section/article/div[1]/div[3]/table/tbody/tr/td[6]/text()')
    volume_ = element.xpath(
        '//*[@id="nimbus-app"]/section/section/section/article/div[1]/div[3]/table/tbody/tr/td[7]/text()')

    for i1, i2, i3, i4, i5, i6, i7 in zip(date_, open_, high_, low_, close_, adj_close, volume_):
        modified_list1 = [item if item != "-" else "" for item in [i1, i2, i3, i4, i5, i6, i7]]
        integer_list = [to_integer(x) for x in modified_list1]
        last_list = [translate_date(integer_list[0])] + integer_list[1:]

        dt_tuple_list.append(tuple(last_list))

    driver.quit()
    insert_into_DB(db_name, table_name, dt_tuple_list)


