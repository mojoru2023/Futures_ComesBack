import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.signal import argrelextrema
import pandas as pd


def animate(i, x, closing_prices, high_points_idx, low_points_idx, ax2):
    """更新每一帧的绘图内容"""
    ax2.clear()

    # 绘制价格曲线
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Price', color='#126ea1')

    ax2.plot(x[:i], closing_prices[:i], label='Closing Prices', color='#126ea1')

    if high_points_idx[high_points_idx < i].size > 0:
        ax2.scatter(high_points_idx[high_points_idx < i],
                    np.array(closing_prices)[high_points_idx][high_points_idx < i],
                    color='red', label='High Points', zorder=5)

    if low_points_idx[low_points_idx < i].size > 0:
        ax2.scatter(low_points_idx[low_points_idx < i],
                    np.array(closing_prices)[low_points_idx][low_points_idx < i],
                    color='green', label='Low Points', zorder=5)

    ax2.tick_params(axis='y', labelcolor='#126ea1')
    ax2.legend(loc='upper left')

    # 添加标题和网格
    ax2.set_title('Dynamic Visualization of Closing Prices')
    ax2.grid()


def read_csv_to_chart(filename, num):
    """
    读取CSV并绘制价格图
    :param filename: CSV文件名
    :param num: 局部极值窗口大小
    :return: None
    """

    # 读取 CSV 文件
    data = pd.read_csv(filename)

    # 提取“終値”列并转换为列表
    closing_prices = data['終値'].tolist()

    # 创建时间序列
    x = np.arange(len(closing_prices))

    # 找到局部高点和低点
    high_points_idx = argrelextrema(np.array(closing_prices), np.greater_equal, order=num)[0]
    low_points_idx = argrelextrema(np.array(closing_prices), np.less_equal, order=num)[0]

    # 创建图形和子图
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12))

    # 绘制静态图
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Price', color='#126ea1')
    ax1.plot(x, closing_prices, label='Closing Prices', color='#126ea1')
    ax1.scatter(high_points_idx, np.array(closing_prices)[high_points_idx], color='red', label='High Points', zorder=5)
    ax1.scatter(low_points_idx, np.array(closing_prices)[low_points_idx], color='green', label='Low Points', zorder=5)
    ax1.plot(high_points_idx, np.array(closing_prices)[high_points_idx], color='red', linestyle='--',
             label='Resistance Line (Highs)')
    ax1.plot(low_points_idx, np.array(closing_prices)[low_points_idx], color='green', linestyle='--',
             label='Support Line (Lows)')
    ax1.tick_params(axis='y', labelcolor='#126ea1')
    ax1.legend(loc='upper left')

    # 添加标题和网格
    ax1.set_title('Static Visualization of Closing Prices')
    ax1.grid()

    # 显示静态图
    plt.tight_layout()
    plt.show(block=False)  # 防止阻塞，允许后续动画绘制

    # 暂停以便查看静态图
    plt.pause(3)  # 停留3秒

    # 创建动画
    ani = FuncAnimation(fig, animate, frames=len(closing_prices),
                        fargs=(x, closing_prices, high_points_idx, low_points_idx, ax2),
                        repeat=False, interval=10)  # 设置较长的间隔以减慢动画速度

    # 显示动画
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    #read_csv_to_chart("day.csv", 6)  # 替换为实际文件路径和参数
    read_csv_to_chart("60m.csv", 10)  # 替换为实际文件路径和参数
    read_csv_to_chart("3m.csv", 100)  # 替换为实际文件路径和参数
