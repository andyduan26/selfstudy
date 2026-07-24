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
