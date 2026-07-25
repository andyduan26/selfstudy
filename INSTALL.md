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

## 邮件通知配置

讲师认证审核通过或驳回时，Django 后台会给申请人的邮箱发送通知。

开发环境默认使用控制台输出：

```text
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

需要真实发送邮件时，在 `backend/.env` 中改为 SMTP，例如 163 邮箱：

```text
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
DEFAULT_FROM_EMAIL=你的邮箱@163.com
EMAIL_HOST=smtp.163.com
EMAIL_PORT=465
EMAIL_HOST_USER=你的邮箱@163.com
EMAIL_HOST_PASSWORD=邮箱授权码
EMAIL_USE_TLS=False
EMAIL_USE_SSL=True
EMAIL_TIMEOUT=10
EMAIL_FAIL_SILENTLY=False
```

QQ 邮箱配置类似：

```text
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
DEFAULT_FROM_EMAIL=你的邮箱@qq.com
EMAIL_HOST=smtp.qq.com
EMAIL_PORT=465
EMAIL_HOST_USER=你的邮箱@qq.com
EMAIL_HOST_PASSWORD=邮箱授权码
EMAIL_USE_TLS=False
EMAIL_USE_SSL=True
```

注意：`EMAIL_HOST_PASSWORD` 填邮箱后台生成的 SMTP 授权码，不是邮箱登录密码。修改后重启 Django 后端，再到后台审核讲师申请即可触发邮件。

如果本机暂时没有 MySQL，可在 `backend/.env` 中设置：

```text
USE_SQLITE_FOR_TESTS=True
```

该开关只用于本地检查和测试，正式开发按 MySQL 配置运行。

## 支付宝沙箱支付配置

课程付费已接入支付宝沙箱电脑网站支付。先在支付宝开放平台沙箱应用中取得参数，再写入 `backend/.env`：

```text
ALIPAY_ENV=sandbox
ALIPAY_APP_ID=你的沙箱 APP_ID
ALIPAY_APP_PRIVATE_KEY=你的应用私钥
ALIPAY_PUBLIC_KEY=支付宝公钥
ALIPAY_NOTIFY_URL=https://你的公网域名/api/orders/alipay-notify/
ALIPAY_RETURN_URL=http://127.0.0.1:5173/user
```

注意：`ALIPAY_NOTIFY_URL` 必须是支付宝服务器能访问的公网 HTTPS 地址。本地 `127.0.0.1` 可以生成支付链接，但支付宝无法回调到你的电脑。开发时可用内网穿透工具把 `127.0.0.1:8000` 暴露成公网地址。

修改后重启 Django 后端。用户在课程详情页点击“开通学习”后，会打开支付宝沙箱收银台；支付成功且异步通知验签通过后，后端才会把订单改为已支付并生成讲师收益。
