# **Beany · FastAPI Demo**

一个现代化、结构清晰、可扩展的 **FastAPI 后端工程模板**。
开箱即用 **用户登录、验证码发送、PostgreSQL、异步 ORM、全局异常处理、依赖注入** 等核心能力。

> 🎯 目标：成为开发者快速构建生产级 FastAPI 后端的优选模板
> ⭐ 欢迎 Star / Fork，一起完善生态！

---

## ✨ **特点亮点**

### 🚀 1. 100% 异步架构

基于 **FastAPI + SQLModel + AsyncSession + PostgreSQL**
支持高并发 & 异步 I/O，性能出色。

### 🏗 2. 企业级项目结构

清晰分层：`router / service / dao / model / common / store / util`
便于团队协作与后期扩展。

### 🔐 3. 开箱即用权限体系

* JWT 鉴权
* OAuth2 token 流程
* 用户登录 / 自动注册
* 验证码登录（邮箱 / 手机）

### 📡 4. 完整的验证码系统

* 支持邮箱 / SMS
* 发送记录入库
* 验证码校验、过期处理
* 基于 Jinja2 的 HTML 邮件模板

### 🧩 5. 稳健的全局异常处理

统一 ResponseModel
支持业务错误、Pydantic 校验错误、全局异常。

### 🔧 6. 高可维护的 DAO 层

通用 BaseDao：增删改查可复用
每个 model 的 dao 只需增加少量业务方法即可。

### 📨 7. SMTP 邮件发送（异步）

aiosmtplib + Jinja2
生产级可扩展能力。

---

## 🏛️ **项目结构说明**

```
beany-fastapi-async
├── common                     # 全局工具：配置、异常、响应模型等
│   ├── common.py
│   ├── config.py
│   └── deps.py                # 全局依赖注入（DB、用户）
│
├── dao                        # 数据访问层（数据库读写操作）
│   ├── base_dao.py
│   ├── user_dao.py
│   └── captcha_dao.py
│
├── model                      # SQLModel 模型 / 请求体定义
│   ├── user.py
│   └── captcha.py
│
├── service                    # 业务逻辑层
│   ├── user_service.py
│   └── captcha_service.py
│
├── router                     # 路由模块
│   ├── user.py
│   ├── captcha.py
│   └── __init__.py
│
├── store                      # 数据库连接、基础模型
│   └── postgres.py
│
├── templates                  # Jinja2 邮件模板
│
├── util                       # 工具函数（token、验证码等）
│   └── utils.py
│
├── main.py                    # 应用入口，注册路由、异常处理
├── pyproject.toml             # 项目依赖（uv）
└── README.md
```

---

## 🚀 **快速开始**

### 1. 安装 uv（推荐）

```bash
pip install uv
```

### 2. 初始化项目

```bash
uv sync
```

### 3. 创建 `.env`

```
APP_NAME=Beany
SECRET_KEY=your-secret-key
ROOT_PATH=/api

DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/dbname

SMTP_HOST=smtp.qq.com
SMTP_EMAIL=xxx@qq.com
SMTP_USER=Beany
SMTP_PASSWORD=xxxx
SMTP_SSL=True
SMTP_TLS=False
SMTP_PORT=465
```

### 4. 运行开发环境

```bash
uv run uvicorn main:app --reload
```

启动后访问：

➡ [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
自动生成的 API 文档（OpenAPI）

---

## 🧪 **内置 API 示例**

### 登录（验证码登录）

```
POST /api/user/login
{
  "account": "email@example.com",
  "code": "123456"
}
```

### 发送验证码

```
POST /api/captcha/send_code
{
  "account": "email@example.com"
}
```

### 获取当前用户

```
GET /api/user/me
Authorization: Bearer <token>
```

---

## 🧬 **技术栈**

| 技术         | 说明                             |
| ---------- | ------------------------------ |
| FastAPI    | 高性能 Python Web 框架              |
| SQLModel   | 结合 Pydantic + SQLAlchemy 的 ORM |
| asyncpg    | PostgreSQL 异步驱动                |
| aiosmtplib | 异步邮件发送                         |
| Jinja2     | 邮件模板渲染                         |
| PyJWT      | token 管理                       |
| uv         | Python 项目与依赖管理                 |

---

## 🌱 **适合谁？**

* 想快速搭建 **生产级 FastAPI 后端** 的开发者
* 希望学习 **项目结构最佳实践**
* 想构建登录/验证码系统的 Web / App 项目
* 想要一个优雅、可扩展的 **开源模板**

---

## 🤝 **参与贡献**

欢迎 Fork / PR，一起让模板更强大 👇👇👇
**Star ⭐ 是对项目最大的支持！**

---

## 📄 License

MIT License

---