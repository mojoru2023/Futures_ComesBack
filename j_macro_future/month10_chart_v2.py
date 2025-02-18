
import sqlite3
from datetime import datetime, timedelta
import plotly.graph_objects as go


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
            cumulative_list.append(cumulative_value)
        monthly_cumulative[month] = cumulative_list

    return monthly_cumulative


def plot_cumulative_curves(monthly_cumulative):
    fig = go.Figure()

    for month, cumulative_values in monthly_cumulative.items():
        # 使用索引作为X坐标
        indices = list(range(len(cumulative_values)))
        fig.add_trace(go.Scatter(x=indices, y=cumulative_values, mode='lines', name=month.strftime('%Y-%m')))

    fig.update_layout(
        title='Monthly Cumulative Fluctuations Over the Last 12 Months',
        xaxis_title='Days of the Month',
        yaxis_title='Cumulative Points',
        showlegend=True,
        hovermode='closest'  # 启用悬浮提示
    )

    fig.show()
    fig.write_html("cumulative_fluctuations.html")


if __name__ == '__main__':
    db_name = 'jp_invest.db'
    table_name = 'nikki225_index'

    # Fetch last 12 months of data from DB
    data = fetch_last_12_months_data(db_name, table_name)

    # Calculate daily cumulative fluctuations
    monthly_cumulative = calculate_daily_cumulative_fluctuation(data)

    # Plot the results
    plot_cumulative_curves(monthly_cumulative)