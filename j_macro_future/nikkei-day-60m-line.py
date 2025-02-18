import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema

import pandas as pd



def read_csv_to_chart(filename,num):
    """

    :param filename:
    :param num:
    :return:
    """


    # 读取 CSV 文件
    file_path = filename  # 替换为实际文件路径
    data = pd.read_csv(file_path)

    # 提取“終値”列并转换为列表
    closing_prices = data['終値'].tolist()


    # 创建时间序列
    x = np.arange(len(closing_prices))

    # 找到局部高点和低点
    # n = 100  # 窗口大小，可调节以增加或减少灵敏度
    # 日线使用n = 6
    high_points_idx = argrelextrema(np.array(closing_prices), np.greater_equal, order=num)[0]
    low_points_idx = argrelextrema(np.array(closing_prices), np.less_equal, order=num)[0]

    # 提取高点和低点的价格
    high_points = np.array(closing_prices)[high_points_idx]  # 使用 np.array 将列表转换为数组
    low_points = np.array(closing_prices)[low_points_idx]    # 使用 np.array 将列表转换为数组

    # 绘制折线图
    plt.figure(figsize=(12, 6))
    # plt.plot(x, closing_prices, label='Closing Prices', color='blue')
    plt.plot(x, closing_prices, label='Closing Prices', color='#126ea1') # 颜色还原日经的原图
    plt.scatter(high_points_idx, high_points, color='red', label='High Points', zorder=5)
    plt.scatter(low_points_idx, low_points, color='green', label='Low Points', zorder=5)

    # 连接高点和低点
    plt.plot(high_points_idx, high_points, color='red', linestyle='--', label='Resistance Line (Highs)')
    plt.plot(low_points_idx, low_points, color='green', linestyle='--', label='Support Line (Lows)')

    # 添加标题和标签
    plt.title('Closing Prices with Support and Resistance Lines')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.legend()
    plt.grid()

    # 显示图形
    plt.show()

if __name__ == "__main__":
    read_csv_to_chart("day.csv",6) # 日线的支撑和压力分析
    read_csv_to_chart("60m.csv",10) # 60分钟的支撑和压力分析
    read_csv_to_chart("3m.csv",100) # 3分钟线的支撑和压力分析