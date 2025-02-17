#!/bin/bash
/etc/init.d/cron start

cd /app || exit 1
python getCookie_web.py >> /proc/1/fd/1 2>> /proc/1/fd/2

#将容器挂起，防止容器后台启动后自动退出
tail -f /dev/null
