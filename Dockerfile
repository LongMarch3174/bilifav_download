# 使用带有 ffmpeg 的官方镜像作为基础镜像
FROM jrottenberg/ffmpeg:7.1-ubuntu2404

RUN sed -i 's@http://archive.ubuntu.com/ubuntu/@http://mirrors.aliyun.com/ubuntu/@g' /etc/apt/sources.list # 更换源

# 设置工作目录
WORKDIR /app

# 更新包列表并安装 Python 3.8 和相关依赖
RUN apt clean && apt update && apt install -y python3
RUN apt install -y python3-dev
RUN apt install -y python3-pip

RUN ln -sf /usr/bin/pip3 /usr/bin/pip && ln -sf /usr/bin/python3 /usr/bin/python

RUN mv /usr/lib/python3.12/EXTERNALLY-MANAGED /usr/lib/python3.12/EXTERNALLY-MANAGED.bk

# 将项目文件复制到容器的工作目录中
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 映射本地文件到容器的工作目录
VOLUME ["/app/bili_videos"]

# 启动交互式 shell，而不是自动执行命令
ENTRYPOINT ["/bin/bash"]