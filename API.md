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

登录账号支持 `username`、邮箱、手机号、昵称，密码为注册时设置的密码。后端只保存加密后的密码哈希，不保存明文密码。

前台注册：

```http
POST /api/users/register/
```

个人资料：

```http
GET /api/users/me/
PATCH /api/users/me/
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

## 视频上传字段

`Video` 模型同时支持三种视频来源：

- `source_type=upload`：使用 `video_file` 上传本地视频文件。
- `source_type=external`：使用 `video_url` 保存外部视频地址。
- `source_type=vod`：使用 `vod_file_id` 保存云点播文件 ID。

辅助字段包含 `poster` 视频封面、`duration_seconds` 时长、`file_size` 文件大小、`transcode_status` 转码状态、`view_count` 点播量、`is_free_preview` 试看标记和 `sort_weight` 排序权重。
