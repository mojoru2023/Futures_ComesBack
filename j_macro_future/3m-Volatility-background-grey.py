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
        vol = calculate_volatility(prices[i - window:i])  # 在窗口内计算波动率
        volatilities.append(vol)
    return [np.nan] * window + volatilities  # 返回与原始价格长度相同的数组，前面补NaN


def read_csv_to_chart(filename, num, volatility_window=20):
    """
    读取CSV并绘制价格和波动率图
    :param filename: CSV文件名
    :param num: 局部极值窗口大小
    :param volatility_window: 计算波动率的窗口大小
    :return: None
    """

    # 读取 CSV 文件
    data = pd.read_csv(filename)

    # 提取“終値”列和“日付”列
    closing_prices = data['終値'].tolist()
    dates = data['日付'].tolist()

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

    # 统计每天的波动率
    daily_volatility_dict = {}
    for i in range(len(closing_prices)):
        date = dates[i]
        if date not in daily_volatility_dict:
            daily_volatility_dict[date] = []
        if i >= volatility_window:  # 确保我们只记录有效的波动率
            daily_volatility_dict[date].append(rolling_volatility[i])

    # 输出每天的波动率数据，并统计大于和小于阈值的比例
    for date, volatilities in daily_volatility_dict.items():
        if volatilities:  # 如果有有效的波动率数据
            count_above = sum(1 for vol in volatilities if vol > v_threshold)  # 统计大于阈值的数量
            count_below = len(volatilities) - count_above  # 统计小于等于阈值的数量
            ratio_above = count_above / len(volatilities)  # 计算大于阈值的比例
            ratio_below = count_below / len(volatilities)  # 计算小于等于阈值的比例

            print(f"日期: {date}  大于 {v_threshold} 的比例: {ratio_above:.2%}  小于等于 {v_threshold} 的比例: {ratio_below:.2%} ")
            # print(f"波动率数据: {volatilities}")

            print("-" * 80)

    # 统计波动率大于和小于阈值的数量（全局统计）
    count_above_threshold = 0
    count_below_threshold = 0
    total_count = 0

    for date, volatilities in daily_volatility_dict.items():
        if volatilities:  # 如果有有效的波动率数据
            avg_volatility = np.nanmean(volatilities)  # 计算平均波动率
            total_count += 1
            if avg_volatility > v_threshold:
                count_above_threshold += 1
            else:
                count_below_threshold += 1

    ratio_above = count_above_threshold / total_count if total_count > 0 else 0
    ratio_below = count_below_threshold / total_count if total_count > 0 else 0

    print(f'全局统计：')
    print(f'波动率大于 {v_threshold} 的比例: {ratio_above:.2%}')
    print(f'波动率小于等于 {v_threshold} 的比例: {ratio_below:.2%}')

    # 绘制折线图
    fig, ax1 = plt.subplots(figsize=(12, 6))

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

    # 设置波动率的纵坐标范围，动态调整
    if len(rolling_volatility) > 0:
        max_volatility = np.nanmax(rolling_volatility)
        min_volatility = np.nanmin(rolling_volatility)
        ax2.set_ylim(max(0, min_volatility * 0.8), min(0.2, max_volatility * 1.2))  # 动态设置最大值
    else:
        ax2.set_ylim(0, 0.2)  # 如果没有数据，默认范围

    ax2.tick_params(axis='y', labelcolor='orange')
    ax2.legend(loc='upper right')

    # 添加背景色处理，当波动率超过v_threshold时
    for i in range(len(rolling_volatility)):
        if rolling_volatility[i] > v_threshold:
            ax1.axvspan(i - 0.5, i + 0.5, color='gray', alpha=0.5)

    # 添加标题和网格
    plt.title(f'Closing Prices with Support and Resistance Lines\n Rolling Volatility')
    ax1.grid()

    # 显示图形
    plt.show()


if __name__ == "__main__":
    v_threshold = 0.0008 # 日内跟盘用这个，避开混沌
    # 当天超过50%就算了，超过30%还能拼一拼 ，2025.3.5 就不该进场的
    # read_csv_to_chart("day.csv", 6)  # 日线的支撑和压力分析
    # read_csv_to_chart("60m.csv", 10)  # 60分钟的
    read_csv_to_chart("3m.csv", 100)  # 3分钟线的支撑和压力分析