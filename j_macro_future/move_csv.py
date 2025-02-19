import os
import shutil
import argparse
import time
from datetime import datetime


def move_and_rename_file(new_file_name, destination_dir):
    # 获取当前日期并格式化为 YYYYMMDD
    current_date = datetime.now().strftime('%Y%m%d')
    source_file = f'futueOptionChart_{current_date}.csv'  # 当前目录下的文件

    # 构建目标文件的完整路径
    destination_file = os.path.join(destination_dir, new_file_name)

    # 移动并重命名文件
    shutil.move(source_file, destination_file)
    print(
        f"File '{source_file}' has been renamed to '{new_file_name}' and moved to '{destination_dir}'.")


def monitor_for_file(new_file_name, destination_dir):
    while True:
        # 获取当前日期并构建源文件名
        current_date = datetime.now().strftime('%Y%m%d')
        source_file = f'futueOptionChart_{current_date}.csv'

        # 检查文件是否存在
        if os.path.isfile(source_file):
            move_and_rename_file(new_file_name, destination_dir)

        # 如果未找到文件，打印提示信息（可选）
        else:
            print(
                f"File '{source_file}' not found, checking again in 10 seconds...")

        # 每 10 秒检查一次
        time.sleep(10)


if __name__ == "__main__":
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(
        description='Rename and move a CSV file when it appears.')

    # 添加参数
    parser.add_argument('new_file_name', type=str,
                        help='The new name for the CSV file')
    parser.add_argument('destination_dir', type=str,
                        help='The destination directory to move the file to')

    # 解析参数
    args = parser.parse_args()

    # 开始监控文件
    monitor_for_file(args.new_file_name, args.destination_dir)
