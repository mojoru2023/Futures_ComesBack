import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from colorama import Fore, Style, init

# 初始化Colorama
init(autoreset=True)

# 设置要请求的URL
url = "https://port.jpx.co.jp/jpx/template/quote.cgi?F=tmp/popchart&QCODE=115.555/O"  # 替换为您想请求的URL

# 初始化Selenium WebDriver并最大化窗口
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.maximize_window()  # 最大化浏览器窗口

try:
    # 输出结果
    # 输出结果（确保列宽一致）
    print(f"\n{'=' * 80}")  # 分隔线
    print(f"| {'Time':<20} | {'现价 1':^20} | {'波动 2':^20} |")
    print(f"{'-' * 80}")
    while True:
        driver.get(url)  # 请求页面

        # 获取需要解析的两个部分
        part1 = driver.find_element("xpath", '//*[@id="readArea"]/div[2]/div/table/tbody/tr[2]/td[6]').text
        part2 = driver.find_element("xpath", '//*[@id="readArea"]/div[2]/div/table/tbody/tr[2]/td[7]').text

        part1_value = part1.split()[0]
        part2_value = float(part2.split()[0])
        # 转换part2为数字以进行比较
        try:
            part2_value = float(part2.split()[0])
        except ValueError:
            part2_value = -1  # 如果转换失败，设为-1

        # 根据part2的值确定颜色
        if part2_value > 0:
            color_part1 = Fore.RED
            color_part2 = Fore.RED
        else:
            color_part1 = Fore.GREEN
            color_part2 = Fore.GREEN

        # 输出结果
        # 获取当前时间
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')

        # 输出结果


        print(f"| {current_time:<20} | {color_part1}{part1_value:<22}{Style.RESET_ALL} | {color_part2}{part2_value:<21}{Style.RESET_ALL} |")
        print(f"{'=' * 80}")


        time.sleep(15)  # 等待30秒


finally:
    driver.close()  # 退出WebDriver  加入到上面的代码中