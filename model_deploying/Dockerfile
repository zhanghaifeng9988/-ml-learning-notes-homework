# 指定基础镜像
# 使用 Python 3.11.16 的 slim 版本（精简版，基于 Debian Bookworm）
FROM python:3.11.16-slim-bookworm
# 在镜像中安装 pipenv（Python 依赖管理工具）
# pipenv 用于根据 Pipfile 和 Pipfile.lock 安装依赖
RUN pip install pipenv -i https://pypi.tuna.tsinghua.edu.cn/simple
# 设置工作目录为 /app
# 后续的 COPY、RUN 等命令都在这个目录下执行
# 如果目录不存在，会自动创建
WORKDIR /app
# 从宿主机复制 Pipfile 和 Pipfile.lock 到镜像的 /app 目录
# [ ] 表示列表格式，可以一次复制多个文件
# "./" 表示当前工作目录（即 /app）
COPY ["Pipfile", "Pipfile.lock", "./"]
# 运行 pipenv install 安装所有依赖
# --system: 安装到系统的 Python 环境，而不是虚拟环境
# --deploy: 严格模式，要求 Pipfile.lock 存在且与 Pipfile 匹配
#           如果版本不匹配，构建会失败（保证可重现）
RUN pipenv install --system --deploy  -i https://pypi.tuna.tsinghua.edu.cn/simple
# 复制业务代码和模型文件到镜像
# prediction1.py: Flask 应用代码
# model_C=1.0.bin: 训练好的机器学习模型文件
COPY ["prediction1.py", "model_C=1.0.bin", "./"]
# 声明容器运行时监听的端口号
# 这只是文档说明，不会实际打开端口
# 真正的端口映射需要在 docker run 时用 -p 参数
EXPOSE 9696
# 设置容器的入口命令
# 容器启动时自动执行 gunicorn，绑定 0.0.0.0:9696
# prediction1:app 表示 prediction1.py 文件中的 app 对象（Flask 实例）
# 这个命令会覆盖 Dockerfile 中的 CMD，但不会被 docker run 的命令行参数覆盖
ENTRYPOINT ["gunicorn", "--bind=0.0.0.0:9696", "prediction1:app"]
