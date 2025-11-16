# ==========================================
#  Stage 1: Build dependencies with uv
# ==========================================
FROM python:3.14-slim AS builder

# 防止 Python 生成 .pyc
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 安装构建依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 安装 uv
RUN pip install uv

WORKDIR /app

# 仅复制依赖声明文件，提高缓存命中率
COPY pyproject.toml .

# 安装依赖（使用 uv）
RUN uv sync --frozen


# ==========================================
#  Stage 2: Runtime Image
# ==========================================
FROM python:3.14-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# 从 builder 拷贝 uv 依赖缓存（加速）
COPY --from=builder /root/.cache/uv /root/.cache/uv
COPY --from=builder /app/.venv /app/.venv

# 配置 PATH 使 .venv 生效
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# 复制项目所有文件
COPY . .

# 暴露 API 端口
EXPOSE 8000

# 使用非 root 用户运行更安全
RUN useradd -m beany
USER beany

# 运行 FastAPI 服务
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
