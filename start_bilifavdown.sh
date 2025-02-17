#!/bin/bash

# 切换到应用目录
cd /app || exit 1  # 如果无法进入/app目录，则退出脚本并返回错误代码 1

# 执行 Python 脚本
python bilifavirousdownload.py >> /proc/1/fd/1 2>> /proc/1/fd/2
