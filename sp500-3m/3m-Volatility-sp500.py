import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema
import pandas as pd

def calculate_volatility(prices):
    """计算价格的波动率"""
    returns = np.diff(prices) / prices[:-1]  # 计算收益率
    volatility = np.std(returns)  # 计算波动率
    return volatility

def calculate_rolling_volatility(prices, window):
    """计算滚动波动率"""
    volatilities = []
    for i in range(window, len(prices)):
        vol = calculate_volatility(prices[i-window:i])  # 在窗口内计算波动率
        volatilities.append(vol)
    # 返回与原始价格长度相同的数组，前面补NaN
    return [np.nan] * window + volatilities

def read_csv_to_chart(filename, num, volatility_window=20):
    """
    读取CSV并绘制价格和波动率图
    :param filename: CSV文件名
    :param num: 局部极值窗口大小
    :param volatility_window: 计算波动率的窗口大小
    :return: None
    """

    # 读取 CSV 文件，使用空格作为分隔符
    data = pd.read_csv(filename, sep='\s+', header=None, names=['<DATE>', '<TIME>', '<OPEN>', '<HIGH>', '<LOW>', '<CLOSE>', '<TICKVOL>', '<VOL>', '<SPREAD>'])

    # 将 "<CLOSE>" 列转换为浮点数
    closing_prices = pd.to_numeric(data['<CLOSE>'], errors='coerce').tolist()

    # 创建时间序列
    x = np.arange(len(closing_prices))

    # 找到局部高点和低点
    high_points_idx = argrelextrema(np.array(closing_prices), np.greater_equal, order=num)[0]
    low_points_idx = argrelextrema(np.array(closing_prices), np.less_equal, order=num)[0]

    # 提取高点和低点的价格
    high_points = np.array(closing_prices)[high_points_idx]
    low_points = np.array(closing_prices)[low_points_idx]

    # 计算滚动波动率
    rolling_volatility = calculate_rolling_volatility(closing_prices, volatility_window)

    # 绘制折线图
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # 绘制价格曲线
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Price', color='#126ea1')
    ax1.plot(x, closing_prices, label='Closing Prices', color='#126ea1')
    ax1.scatter(high_points_idx, high_points, color='red', label='High Points', zorder=5)
    ax1.scatter(low_points_idx, low_points, color='green', label='Low Points', zorder=5)
    ax1.plot(high_points_idx, high_points, color='red', linestyle='--', label='Resistance Line (Highs)')
    ax1.plot(low_points_idx, low_points, color='green', linestyle='--', label='Support Line (Lows)')
    ax1.tick_params(axis='y', labelcolor='#126ea1')
    ax1.legend(loc='upper left')

    # 创建第二个y轴，绘制滚动波动率
    ax2 = ax1.twinx()
    ax2.set_ylabel('Rolling Volatility', color='orange')
    ax2.plot(x, rolling_volatility, color='orange', label='Rolling Volatility', linewidth=2)
    ax2.tick_params(axis='y', labelcolor='orange')

    # 设置波动率的纵坐标范围，动态调整
    if len(rolling_volatility) > 0:
        max_volatility = np.nanmax(rolling_volatility)
        min_volatility = np.nanmin(rolling_volatility)
        ax2.set_ylim(max(0, min_volatility * 0.8), min(0.2, max_volatility * 1.2))  # 动态设置最大值
    else:
        ax2.set_ylim(0, 0.2)  # 如果没有数据，默认范围

    ax2.legend(loc='upper right')

    # 添加标题和网格
  # 添加标题和网格
    plt.title(f'Closing Prices with Support and Resistance Lines\nRolling Volatility')
    ax1.grid()

    # 显示图形
    plt.show()

if __name__ == "__main__":
    read_csv_to_chart("3m.csv", num=100)  # 这里可以根据需要调整 `num` 的值