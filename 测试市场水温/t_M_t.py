
#! -*- utf-8 -*-

import datetime
from itertools import chain
import pymysql
from queue import Queue
import threading
import time

from lxml import etree

# selenium 3.12.0
from selenium.webdriver import PhantomJS








def test_M_temp():
    url = "http://quote.eastmoney.com/gb/zsN225.html"
    ch_options = PhantomJS("C:\\Python310\\Scripts\\phantomjs.exe")  # windows
    ch_options.get(url)
    time.sleep(1)
    html = ch_options.page_source
    ch_options.close()
    selector = etree.HTML(html)
    last_price = selector.xpath('//*[@id="app"]/div/div/div[8]/div[1]/div/div[1]/span[1]/span/text()')
    open_price = selector.xpath('//*[@id="app"]/div/div/div[7]/div[2]/ul[1]/li[1]/span[2]/span/text()')
    max_price = selector.xpath('//*[@id="app"]/div/div/div[7]/div[2]/ul[1]/li[3]/span[2]/span/text()')
    min_price = selector.xpath('//*[@id="app"]/div/div/div[7]/div[2]/ul[1]/li[4]/span[2]/span/text()')

    max_min = int(max_price[0]) -int(min_price[0])
    max_open = int(max_price[0]) -int(open_price[0])
    min_open = int(min_price[0]) -int(open_price[0])
    last_open = int(last_price[0]) -int(open_price[0])
    return max_min,max_open,min_open,last_open





if __name__=="__main__":
    max_min, max_open, min_open, last_open = test_M_temp()











