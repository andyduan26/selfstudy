# 安装说明

## 环境要求

- Node.js 18 或以上
- npm
- Python 3.9 或以上
- MySQL 8 或以上
- Pillow 图像处理依赖会随 `requirements.txt` 安装，用于头像、封面等上传字段。
- SimpleUI 会随 `requirements.txt` 安装，用于 Django 中文后台界面。

## 本地运行

```bash
npm install
cp .env.example .env
npm run dev
```

默认访问地址：

```text
http://127.0.0.1:5173
```

## 后端运行

```bash
cd backend
cp .env.example .env
.venv/bin/python manage.py migrate
.venv/bin/python manage.py createsuperuser
.venv/bin/python manage.py runserver 127.0.0.1:8000
```

上传文件保存目录：

```text
backend/media/
```

当前邮件通知使用控制台输出。生产环境可在 `backend/.env` 中配置 SMTP 邮件服务。

如果本机暂时没有 MySQL，可在 `backend/.env` 中设置：

```text
USE_SQLITE_FOR_TESTS=True
```

该开关只用于本地检查和测试，正式开发按 MySQL 配置运行。
