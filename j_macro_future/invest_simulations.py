import random
import matplotlib.pyplot as plt

def simulate_investment(initial_investment, num_simulations):
    total_profit = 0
    profits = []
    cumulative_returns = []  # 用于记录所有模拟的累计收益率

    for _ in range(num_simulations):
        investment = initial_investment
        loss_count = 0
        history = []  # 用于记录每次投资的变化
        # 给出3浮亏后盈利
        while True:
            # 2025.3.5 一个月，半年后再反思
            # 随机选择1到3次亏损，之后盈利
            # 这种模拟可能更接近实战一些 100次，浮盈10倍 200次，浮盈25倍
            # 独立同分布 ，所以也别怕试错3%
            # 每月 20*3=60  3-3.5倍
            # 半年 360 20-30倍
            # 一年 720 40-50倍
            # 所以眼下的100点坚决要止损！ 同时近3次大幅度的预期收益证明，还是完全可以用盈利也养一养亏损的！
            # 1个预期收益在3倍左右，算上了亏损  这种还是比较接近于现实一些
            #绝对需要积累足够的交易次数的，跟盘等都是为了提高胜率，但是一旦站住脚了一定要拿住啊！
            # 因为下一次进场又是重新面临市场的考验！

            #

            if loss_count < 2:  # 前两次亏损
                investment *= (1 - 0.03)  # 亏损3%
                loss_count += 1
            else:  # 每次亏损2到3次后盈利
                if loss_count == 2:  # 第三次盈利6%
                    investment *= (1 + 0.06)
                elif loss_count == 3:  # 第四次盈利10%
                    investment *= (1 + 0.10)
                elif loss_count == 4:  # 第五次盈利20%
                    investment *= (1 + 0.20)
                elif loss_count == 5:  # 第五次盈利20%
                    investment *= (1 + 0.30)

                # 随机决定继续亏损或者结束
                if random.choice([True, False]):
                    loss_count = random.randint(1, 3)  # 随机设置下次亏损次数为1到3
                else:
                    break  # 结束当前模拟

            # 记录每次的投资金额
            history.append(investment)

            # 模拟结束条件，这里设定为投资总额小于500元或大于2倍
            if investment <= initial_investment * 0.5 or investment >= initial_investment * 2:
                break

        total_profit += investment
        profits.append(history)  # 保存这一轮的历史数据

        # 计算并保存收益率
        return_rate = (investment - initial_investment) / initial_investment
        cumulative_returns.append(return_rate)

    average_profit = total_profit / num_simulations
    average_return_rate = sum(cumulative_returns) / num_simulations  # 平均收益率
    return average_profit, profits, cumulative_returns, average_return_rate

# 设置初始投资金额和模拟次数
initial_investment = 1000  # 初始投资1000元
num_simulations = 2000  # 模拟50次

average_profit, profits, cumulative_returns, average_return_rate = simulate_investment(initial_investment, num_simulations)

# 可视化投资变化
for i, history in enumerate(profits):
    plt.plot(history, label=f'Simulation {i + 1}')

plt.title('Investment Simulation Over Time')
plt.xlabel('Steps')
plt.ylabel('Investment Value (元)')

plt.legend()
plt.grid()
plt.show()

# 计算累计收益率
cumulative_sum = [sum(cumulative_returns[:i+1]) for i in range(num_simulations)]

# 可视化累计收益率
plt.figure(figsize=(10, 5))
plt.plot(range(1, num_simulations + 1), cumulative_sum, marker='o', color='skyblue', label='Cumulative Returns')
plt.title('Cumulative Returns Over Simulations')
plt.xlabel('Simulation Number')
plt.ylabel('Cumulative Return Rate')

plt.legend()
plt.grid()
plt.show()

print(f'预期收益: {average_profit:.2f} 元')
print(f'平均收益率: {average_return_rate:.2%}')
