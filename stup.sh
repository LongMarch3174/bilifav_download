#!/bin/bash
/etc/init.d/cron start
#将容器挂起，防止容器后台启动后自动退出
tail -f /dev/null
