# 使用带有 ffmpeg 的官方镜像作为基础镜像
FROM jrottenberg/ffmpeg:7.1-ubuntu2404

RUN sed -i 's@http://archive.ubuntu.com/ubuntu/@http://mirrors.aliyun.com/ubuntu/@g' /etc/apt/sources.list # 更换源

# 设置工作目录
WORKDIR /app

# 更新包列表并安装 Python 3.8 和相关依赖
RUN apt clean && apt update && apt install -y python3 python3-dev python3-pip \
    && ln -sf /usr/bin/pip3 /usr/bin/pip && ln -sf /usr/bin/python3 /usr/bin/python \
    && mv /usr/lib/python3.12/EXTERNALLY-MANAGED /usr/lib/python3.12/EXTERNALLY-MANAGED.bk \
    && apt install -y sqlite3 libsqlite3-dev cron

# 将项目文件复制到容器的工作目录中
COPY . /app
COPY crontab /etc/cron.d/my-cron-job

RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

RUN mkdir /db && /usr/bin/sqlite3 /db/bilibili_downloader.db && chmod 0644 /etc/cron.d/my-cron-job \
    && crontab /etc/cron.d/my-cron-job

# 映射本地文件到容器的工作目录
VOLUME ["/app/bili_videos"]

# 启动 cron 和 Python 脚本
CMD ["cron", "-f"]