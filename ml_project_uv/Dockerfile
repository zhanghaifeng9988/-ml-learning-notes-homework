FROM agrigorev/zoomcamp-model:2025

WORKDIR /app

# 复制项目文件
COPY pyproject.toml README.md ./
COPY src/ ./src/

# 安装项目及其依赖，安装的依赖信息，直接来自于 pyproject.toml 文件
RUN pip install --no-cache-dir .

# 5. 复制应用代码
COPY serve.py ./
COPY pipeline_v1.bin ./

# 6. 暴露端口
EXPOSE 9008

# 7. 启动命令,
# 如果没有ENTRYPOINT——它就是容器启动时的唯一主命令。
# 如果有ENTRYPOINT——ENTRYPOINT就是容器启动时的唯一主命令，CMD则可以作为ENTRYPOINT的参数。
CMD ["uvicorn", "serve:app", "--host", "0.0.0.0", "--port", "9008"]