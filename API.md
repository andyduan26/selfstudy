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

## 前端数据说明

首页课程区、课程列表、课程详情、播放页、个人中心作品和收益均已接入 Django 后端接口。讲师榜单仍保留本地展示数据，后续可继续接后端。

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

课程支付：

```http
POST /api/orders/checkout/
POST /api/orders/alipay-notify/
```

`POST /api/orders/checkout/` 需要登录，参数：

```json
{
  "course_id": 1,
  "pay_method": "alipay"
}
```

免费课程会直接开通；付费课程会返回 `payment_url`，前端打开支付宝沙箱收银台。支付宝异步通知 `POST /api/orders/alipay-notify/` 验签成功后，后端更新订单为已支付并生成讲师收益。

课程评论：

```http
GET /api/comments/?course=1
POST /api/comments/
```

评论提交后直接显示，不需要后台审核。

讲师申请与作品上传：

```http
POST /api/teacher-applications/
POST /api/courses/upload-work/
```

`POST /api/teacher-applications/` 支持 `multipart/form-data`，字段包含 `real_name`、`phone`、`direction`、`experience`、`portfolio_url`、`sample_video`、`certificate_file`。

`POST /api/courses/upload-work/` 仅认证讲师可用，支持课程封面 `cover`、课程视频 `video_file`、课程附件 `attachment_file`。后端会保存到 `backend/media/`，课程状态默认为待审核。

## 视频上传字段

`Video` 模型同时支持三种视频来源：

- `source_type=upload`：使用 `video_file` 上传本地视频文件。
- `source_type=external`：使用 `video_url` 保存外部视频地址。
- `source_type=vod`：使用 `vod_file_id` 保存云点播文件 ID。

辅助字段包含 `poster` 视频封面、`duration_seconds` 时长、`file_size` 文件大小、`transcode_status` 转码状态、`view_count` 点播量、`is_free_preview` 试看标记和 `sort_weight` 排序权重。

HLS 播放字段：

- `hls_url`：HLS 播放地址，前端播放页优先使用。
- `hls_path`：本地 HLS 切片目录。
- `source_type=hls`：表示该视频已完成 HLS 转码。

手动转码接口使用 Django 管理命令：

```bash
python manage.py transcode_hls --pending
```

R2 上传：

```bash
python manage.py transcode_hls --upload-r2-only
python manage.py transcode_hls --video-id 1 --upload-r2-only
```

当 `R2_ACCOUNT_ID`、`R2_ACCESS_KEY_ID`、`R2_SECRET_ACCESS_KEY`、`R2_BUCKET_NAME`、`R2_PUBLIC_BASE_URL` 配置完整时，转码完成会自动上传 HLS 文件到 Cloudflare R2，并把 `hls_url` 更新为 R2 公网地址。

大文件上传配置：

```text
DATA_UPLOAD_MAX_MEMORY_SIZE=1073741824
FILE_UPLOAD_MAX_MEMORY_SIZE=104857600
```

当前适合本地和中小规模上传。生产环境建议接对象存储或云点播直传。
