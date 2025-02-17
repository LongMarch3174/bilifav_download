# 使用带有 ffmpeg 的官方镜像作为基础镜像
FROM jrottenberg/ffmpeg:7.1-ubuntu2404

# 设置工作目录
WORKDIR /app

# 更新包列表并安装 Python 3.8 和相关依赖
RUN apt update && \
    apt install -y \
    python3 \
    python3-dev \
    python3-pip

# 设置默认 python 指令为 python3.8
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.8 1

# 确保 pip 是最新版本
RUN python -m pip install --upgrade pip

# 将项目文件复制到容器的工作目录中
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 映射本地文件到容器的工作目录
VOLUME ["/app/bili_videos"]

# 启动交互式 shell，而不是自动执行命令
ENTRYPOINT ["/bin/bash"]