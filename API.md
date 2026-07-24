# API 说明

## 请求配置

- 基础地址：`VITE_API_BASE_URL`
- 请求封装：`src/api/request.js`
- Token 头：`Authorization: Bearer <token>`

## 预留接口

### 获取当前用户

```http
GET /api/users/me/
```

当前阶段只完成前端架构，不实现具体业务接口。

## 静态页面说明

课程、讲师、榜单、试看状态均来自 `src/data/platform.js`，当前不请求后端接口。

## 后端 API

JWT 登录：

```http
POST /api/auth/token/
POST /api/auth/token/refresh/
```

核心资源：

```text
/api/users/
/api/users/me/
/api/teacher-profiles/
/api/teacher-applications/
/api/categories/
/api/courses/
/api/chapters/
/api/videos/
/api/orders/
/api/revenues/
/api/withdrawals/
/api/comments/
/api/favorites/
```
