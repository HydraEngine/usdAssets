#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

import os
import subprocess

if __name__ == '__main__':
    # 获取当前目录
    current_directory = os.getcwd()

    # 遍历当前目录中的所有文件
    for filename in os.listdir(current_directory):
        # 检查文件是否是Python文件
        if filename.endswith('.py'):
            if filename == "generate_all.py":
                continue

            file_path = os.path.join(current_directory, filename)
            print(f'generated by: {file_path}')
            # 运行Python文件
            subprocess.run(['python3', file_path])