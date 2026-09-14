## 为 AWS Lambda 函数构建容器镜像的配置

# 基础镜像
FROM public.ecr.aws/lambda/python:3.13
# 安装 uv（从官方镜像复制二进制文件，比 pip 安装uv更快更干净）
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

# 复制依赖文件，复制到镜像的工作目录 /var/task
COPY pyproject.toml uv.lock ./

# 导出锁定的依赖列表（排除项目本身），并安装到系统 Python
# --no-emit-project  不要把项目本身写进导出结果，只导出它依赖的第三方库。
RUN uv export --format requirements-txt --no-emit-project > requirements.txt && \
    uv pip install --system --no-cache -r requirements.txt && \
    rm requirements.txt

COPY model.bin .

COPY lambda_function.py .

# 设置入口点：告诉 Lambda 运行时，函数入口是 lambda_function 模块中的 lambda_handler 函数。
# 容器启动时，运行时接口会调用这个处理函数。
CMD ["lambda_function.lambda_handler"]