# ==========================================
# Stage 1: Build dependencies with uv
# ==========================================
FROM python:3.14-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 安装构建依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl libffi-dev libssl-dev git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 安装 uv
RUN pip install --no-cache-dir uv

WORKDIR /app

# 复制依赖文件
COPY pyproject.toml uv.lock ./

# 安装依赖（使用 uv 虚拟环境）
RUN uv sync --frozen

# ==========================================
# Stage 2: Runtime image
# ==========================================
FROM python:3.14-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# 从 builder 拷贝 uv 虚拟环境
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /root/.cache/uv /root/.cache/uv

# 配置 PATH 让虚拟环境生效
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# 复制项目代码
COPY . .

# 暴露端口
EXPOSE 8000

# 使用非 root 用户
RUN useradd -m beany
USER beany

# 启动 FastAPI
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
