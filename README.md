# 我要自学网前端

基于 Vue3、Vite、Vue Router、Pinia、Axios、Element Plus 的前端，以及 Django、DRF、JWT、MySQL 的后端基础架构。

当前已包含知识分享平台静态页面：首页、课程分类、课程详情、视频播放、讲师公开主页、登录注册、个人中心。

后端位于 `backend/`，已包含用户、讲师申请、课程作品、章节视频、订单、收益、提现、评论收藏等核心数据模型。

Django 根路径会跳转到 Vue 前端；真实后台使用 SimpleUI 中文管理界面，地址为 `http://127.0.0.1:8000/admin/`。

## 启动

```bash
npm install
npm run dev
```

后端启动：

```bash
cd backend
cp .env.example .env
.venv/bin/python manage.py migrate
.venv/bin/python manage.py runserver
```

## 构建

```bash
npm run build
```

## 部署

- 前端：Vercel，使用 `vercel.json`，构建输出 `dist`。
- 后端：Railway，使用 `backend/Procfile`、`backend/nixpacks.toml` 和 PostgreSQL。
- 视频：Cloudflare R2，HLS 地址保存在 `Video.hls_url`。

上线时前端设置：

```text
VITE_API_BASE_URL=https://你的-railway-后端域名
```

后端设置：

```text
DJANGO_DEBUG=False
DATABASE_URL=Railway PostgreSQL 地址
CORS_ALLOWED_ORIGINS=https://你的-vercel-前端域名
FRONTEND_URL=https://你的-vercel-前端域名/
```

## 目录

```text
src
├── api              # Axios 请求封装与接口模块
├── components       # 公共组件
├── data             # 静态演示数据
├── layouts          # 页面布局
├── router           # 路由与权限守卫
├── stores           # Pinia 状态管理
├── styles           # 全局样式
└── views            # 页面视图
backend
├── config           # Django 项目配置
└── core             # 知识平台核心业务模型与接口
```
