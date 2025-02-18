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

    # 计算每条曲线的最大波动
    max_fluctuations = {month: max(cumulative_values) for month, cumulative_values in monthly_cumulative.items()}

    # 按照波动大小排序，找到最大波动的两条曲线
    sorted_months = sorted(max_fluctuations.items(), key=lambda x: x[1], reverse=True)
    highlight_months = set(month for month, _ in sorted_months[:2])  # 获取最大波动的两条
    recent_month = sorted(monthly_cumulative.keys())[-1]  # 获取最近一条

    # 定义颜色列表（确保每条曲线都有唯一颜色）
    colors = ['#014955', '#1687a7', '#e4d1d3', '#dd0a35',
              '#ff8a5c', '#49beb7', '#badfdb', '#fcf9ea',
              '#7899dc', '#0fefbd', '#feff92', '#cff800']

    for i, (month, cumulative_values) in enumerate(monthly_cumulative.items()):
        # 确定曲线的颜色
        color = colors[i % len(colors)]

        # 高亮显示最大波动的曲线和最近的曲线
        if month in highlight_months or month == recent_month:
            color = 'red'  # 高亮颜色为红色

        # 使用索引作为X坐标
        indices = list(range(len(cumulative_values)))
        fig.add_trace(go.Scatter(x=indices, y=cumulative_values, mode='lines', name=month.strftime('%Y-%m'),
                                 line=dict(color=color)))

    fig.update_layout(
        title='Monthly Cumulative Fluctuations Over the Last 12 Months',
        xaxis_title='Days of the Month',
        yaxis_title='Cumulative Points',
        showlegend=True,
        hovermode='closest',  # 启用悬浮提示
        paper_bgcolor='#142d4c',  # 设置纸张背景颜色
        plot_bgcolor='#142d4c',   # 设置图表背景颜色
        font=dict(color='black')   # 设置字体颜色为白色
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