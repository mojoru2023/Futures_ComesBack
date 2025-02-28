import pandas as pd

# 从 aa.csv 文件读取数据
df = pd.read_csv('3m.csv', sep="\t")

# 处理日期，提取年份和月份
df['<DATE>'] = pd.to_datetime(df['<DATE>'], format='%Y.%m.%d')
df['YearMonth'] = df['<DATE>'].dt.to_period('M')

# 按照年份和月份分组，并输出到不同的 CSV 文件
for period, group in df.groupby('YearMonth'):
    filename = f"{period}.csv"
    group.drop(columns='YearMonth', inplace=True)  # 不包含分组列
    group.to_csv(filename, index=False, sep="\t", header=True)
    print(f"Saved: {filename}")
