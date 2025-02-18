

#               open      high      low   close    volume
# 2017-01-03  115.80  116.3300  114.760  116.15  28781865
# 2017-01-04  115.85  116.5100  115.750  116.02  21118116
# 2017-01-05  115.92  116.8642  115.810  116.61  22193587
# 2017-01-06  116.78  118.1600  116.470  117.91  31751900
# 2017-01-09  117.95  119.4300  117.940  118.99  33561948
# ...            ...       ...      ...     ...       ...
# 2017-12-22  174.68  175.4240  174.500  175.01  16052615
# 2017-12-26  170.80  171.4700  169.679  170.57  32968167
# 2017-12-27  170.10  170.7800  169.710  170.60  21672062
# 2017-12-28  171.00  171.8500  170.480  171.08  15997739
# 2017-12-29  170.52  170.5900  169.220  169.23  25643711
#
# [251 rows x 5 columns]
# mplfinance，一个超酷的 python 库  https://mp.weixin.qq.com/s/08xnm3XXXn49TWaEHFsqDg


# 后面数据积累一段时间再说

# 得先按照要


import pandas as pd
import mplfinance as mpf

import time
import matplotlib.pyplot as plt

infile = 'dd.csv'

df = pd.read_csv(infile, index_col=0, parse_dates=True)

# print('len(df)=',len(df))


for jj in (0,1,2):
    start = jj*35
    stop  = start + 35
    tdf = df.iloc[start:stop]
    fig,_ = mpf.plot(tdf,type='candle',volume=True,mav=(10,20),figscale=1.5,returnfig=True)
    plt.pause(4)
    plt.close(fig)
    del fig
