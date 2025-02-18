import sqlite3
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt


def fetch_last_12_months_data(dbname, tbname):
    connection = sqlite3.connect(dbname)
    cursor = connection.cursor()

    # 获取当前日期
    today = datetime.now()

    # 获取12个月前的日期
    last_year_date = today - timedelta(days=365)

    # 查询过去12个月的数据
    cursor.execute(f'''
        SELECT date_, open_, close_ FROM {tbname}
        WHERE date_ >= ?
        ORDER BY date_ ASC
    ''', (last_year_date.strftime('%Y-%m-%d'),))

    rows = cursor.fetchall()
    connection.close()
    return rows


def calculate_daily_cumulative_fluctuation(data):
    monthly_fluctuations = {}

    for row in data:
        date_str, open_price, close_price = row
        date = datetime.strptime(date_str, '%Y-%m-%d')

        month_key = date.replace(day=1)  # 使用月份的第一天作为键

        if month_key not in monthly_fluctuations:
            monthly_fluctuations[month_key] = []

        # 计算当天的波动（收盘价 - 开盘价）
        daily_fluctuation = float(close_price) - float(open_price)
        monthly_fluctuations[month_key].append((date, daily_fluctuation))

    # 计算每个月的累计值
    monthly_cumulative = {}
    for month, fluctuations in monthly_fluctuations.items():
        cumulative_value = 0
        cumulative_list = []
        for date, fluctuation in fluctuations:
            cumulative_value += fluctuation
            cumulative_list.append((date, cumulative_value))

        # 确保每条曲线的起点为0
        if cumulative_list:
            first_date = cumulative_list[0][0]
            cumulative_list = [(first_date, 0)] + cumulative_list  # 添加起点(0)

        monthly_cumulative[month] = cumulative_list

    return monthly_cumulative


def plot_cumulative_curves(monthly_cumulative):
    plt.figure(figsize=(12, 6))

    for month, cumulative_values in monthly_cumulative.items():
        dates = [date for date, _ in cumulative_values]
        cumulative_points = [value for _, value in cumulative_values]

        plt.plot(dates, cumulative_points, label=month.strftime('%Y-%m'))

    plt.title('SP500:Monthly Cumulative Fluctuations Over the Last 12 Months')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Points')
    plt.axhline(0, color='black', linewidth=0.8, linestyle='--')  # 添加y=0的水平线
    plt.legend()
    plt.xticks(rotation=45)
    plt.grid()
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    db_name = 'us_invest.db'
    table_name = 'sp500_index'

    # Fetch last 12 months of data from DB
    data = fetch_last_12_months_data(db_name, table_name)

    # Calculate daily cumulative fluctuations
    monthly_cumulative = calculate_daily_cumulative_fluctuation(data)

    # Plot the results
    plot_cumulative_curves(monthly_cumulative)
