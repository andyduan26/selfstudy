from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser):
    class Role(models.TextChoices):
        USER = 'user', '普通用户'
        TEACHER = 'teacher', '认证讲师'
        ADMIN = 'admin', '管理员'

    id = models.AutoField(primary_key=True)
    role = models.CharField('身份', max_length=20, choices=Role.choices, default=Role.USER)
    phone = models.CharField('手机号', max_length=20, blank=True, db_index=True)
    avatar = models.ImageField('头像上传', upload_to='avatars/%Y/%m/', blank=True)
    avatar_url = models.URLField('外部头像地址', blank=True)
    bio = models.CharField('简介', max_length=255, blank=True)
    is_verified_teacher = models.BooleanField('是否认证讲师', default=False)
    sort_weight = models.IntegerField('排序权重', default=0)

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'
        ordering = ['-date_joined']

    def __str__(self):
        return self.username


class TeacherProfile(TimeStampedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='teacher_profile', verbose_name='用户')
    real_name = models.CharField('真实姓名', max_length=50)
    title = models.CharField('讲师头衔', max_length=100, blank=True)
    direction = models.CharField('授课方向', max_length=100)
    intro = models.TextField('讲师介绍', blank=True)
    experience = models.TextField('教学/项目经历', blank=True)
    revenue_share_rate = models.DecimalField('讲师分成比例', max_digits=5, decimal_places=2, default=70.00)
    total_students = models.PositiveIntegerField('累计学员', default=0)
    total_revenue = models.DecimalField('累计收益', max_digits=12, decimal_places=2, default=0)
    sort_weight = models.IntegerField('排序权重', default=0)

    class Meta:
        verbose_name = '讲师档案'
        verbose_name_plural = '讲师档案'
        ordering = ['-sort_weight', '-created_at']

    def __str__(self):
        return self.real_name


class TeacherApplication(TimeStampedModel):
    class Status(models.TextChoices):
        PENDING = 'pending', '待审核'
        APPROVED = 'approved', '已通过'
        REJECTED = 'rejected', '已驳回'
        NEED_MORE = 'need_more', '待补充'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='teacher_applications', verbose_name='申请用户')
    real_name = models.CharField('真实姓名', max_length=50)
    phone = models.CharField('联系方式', max_length=30)
    direction = models.CharField('授课方向', max_length=100)
    experience = models.TextField('教学经历')
    portfolio_url = models.URLField('代表作品链接', blank=True)
    sample_video = models.FileField('试讲视频上传', upload_to='teacher_applications/videos/%Y/%m/', blank=True)
    certificate_file = models.FileField('资质证明上传', upload_to='teacher_applications/certificates/%Y/%m/', blank=True)
    status = models.CharField('审核状态', max_length=20, choices=Status.choices, default=Status.PENDING, db_index=True)
    audit_remark = models.TextField('审核备注', blank=True)
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='reviewed_teacher_applications', verbose_name='审核人')
    reviewed_at = models.DateTimeField('审核时间', null=True, blank=True)

    class Meta:
        verbose_name = '讲师申请'
        verbose_name_plural = '讲师申请'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.real_name} - {self.direction}'


class CourseCategory(TimeStampedModel):
    name = models.CharField('分类名称', max_length=50, unique=True)
    slug = models.SlugField('分类标识', max_length=80, unique=True)
    description = models.CharField('分类描述', max_length=255, blank=True)
    sort_weight = models.IntegerField('排序权重', default=0)
    is_active = models.BooleanField('是否启用', default=True)

    class Meta:
        verbose_name = '课程分类'
        verbose_name_plural = '课程分类'
        ordering = ['-sort_weight', 'id']

    def __str__(self):
        return self.name


class Course(TimeStampedModel):
    class Status(models.TextChoices):
        DRAFT = 'draft', '草稿'
        PENDING = 'pending', '待审核'
        APPROVED = 'approved', '已通过'
        REJECTED = 'rejected', '已驳回'
        PUBLISHED = 'published', '已发布'
        OFFLINE = 'offline', '已下架'

    class Level(models.TextChoices):
        BEGINNER = 'beginner', '入门'
        INTERMEDIATE = 'intermediate', '进阶'
        ADVANCED = 'advanced', '实战'

    teacher = models.ForeignKey(TeacherProfile, on_delete=models.PROTECT, related_name='courses', verbose_name='讲师')
    category = models.ForeignKey(CourseCategory, on_delete=models.PROTECT, related_name='courses', verbose_name='分类')
    title = models.CharField('课程标题', max_length=150)
    subtitle = models.CharField('副标题', max_length=255, blank=True)
    cover = models.ImageField('封面图上传', upload_to='courses/covers/%Y/%m/', blank=True)
    cover_url = models.URLField('外部封面地址', blank=True)
    description = models.TextField('课程介绍', blank=True)
    level = models.CharField('难度', max_length=20, choices=Level.choices, default=Level.BEGINNER)
    status = models.CharField('审核/发布状态', max_length=20, choices=Status.choices, default=Status.DRAFT, db_index=True)
    price = models.DecimalField('定价', max_digits=10, decimal_places=2, default=0)
    original_price = models.DecimalField('划线价', max_digits=10, decimal_places=2, default=0)
    is_free = models.BooleanField('是否免费', default=False)
    allow_preview = models.BooleanField('是否允许试看', default=True)
    view_count = models.PositiveIntegerField('点播量', default=0)
    sales_count = models.PositiveIntegerField('销量', default=0)
    favorite_count = models.PositiveIntegerField('收藏数', default=0)
    rating = models.DecimalField('评分', max_digits=3, decimal_places=2, default=0)
    platform_share_rate = models.DecimalField('平台分成比例', max_digits=5, decimal_places=2, default=30.00)
    teacher_share_rate = models.DecimalField('讲师分成比例', max_digits=5, decimal_places=2, default=70.00)
    sort_weight = models.IntegerField('排序权重', default=0)
    audit_remark = models.TextField('审核备注', blank=True)
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='reviewed_courses', verbose_name='审核人')
    reviewed_at = models.DateTimeField('审核时间', null=True, blank=True)
    published_at = models.DateTimeField('发布时间', null=True, blank=True)

    class Meta:
        verbose_name = '课程作品'
        verbose_name_plural = '课程作品'
        ordering = ['-sort_weight', '-created_at']
        indexes = [
            models.Index(fields=['status', 'sort_weight']),
            models.Index(fields=['category', 'status']),
        ]

    def __str__(self):
        return self.title


class Chapter(TimeStampedModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='chapters', verbose_name='课程')
    title = models.CharField('章节标题', max_length=150)
    summary = models.CharField('章节简介', max_length=255, blank=True)
    sort_weight = models.IntegerField('排序权重', default=0)
    is_free_preview = models.BooleanField('是否试看章节', default=False)

    class Meta:
        verbose_name = '课程章节'
        verbose_name_plural = '课程章节'
        ordering = ['sort_weight', 'id']

    def __str__(self):
        return self.title


class Video(TimeStampedModel):
    class SourceType(models.TextChoices):
        UPLOAD = 'upload', '本地上传'
        EXTERNAL = 'external', '外部地址'
        VOD = 'vod', '云点播'

    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='videos', verbose_name='章节')
    title = models.CharField('视频标题', max_length=150)
    source_type = models.CharField('视频来源', max_length=20, choices=SourceType.choices, default=SourceType.UPLOAD)
    video_file = models.FileField('视频文件上传', upload_to='courses/videos/%Y/%m/', blank=True)
    video_url = models.URLField('外部视频地址', blank=True)
    vod_file_id = models.CharField('云点播文件ID', max_length=120, blank=True)
    transcode_status = models.CharField('转码状态', max_length=30, default='pending')
    file_size = models.PositiveBigIntegerField('文件大小字节', default=0)
    duration_seconds = models.PositiveIntegerField('视频时长秒', default=0)
    poster = models.ImageField('视频封面上传', upload_to='courses/video_posters/%Y/%m/', blank=True)
    sort_weight = models.IntegerField('排序权重', default=0)
    is_free_preview = models.BooleanField('是否试看视频', default=False)
    view_count = models.PositiveIntegerField('点播量', default=0)

    class Meta:
        verbose_name = '章节视频'
        verbose_name_plural = '章节视频'
        ordering = ['sort_weight', 'id']

    def __str__(self):
        return self.title


class Order(TimeStampedModel):
    class Status(models.TextChoices):
        PENDING = 'pending', '待支付'
        PAID = 'paid', '已支付'
        CANCELLED = 'cancelled', '已取消'
        REFUNDING = 'refunding', '退款中'
        REFUNDED = 'refunded', '已退款'
        COMPLETED = 'completed', '已完成'

    class PayMethod(models.TextChoices):
        WECHAT = 'wechat', '微信'
        ALIPAY = 'alipay', '支付宝'
        BANK = 'bank', '银行卡'
        FREE = 'free', '免费'

    order_no = models.CharField('订单号', max_length=64, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='orders', verbose_name='用户')
    course = models.ForeignKey(Course, on_delete=models.PROTECT, related_name='orders', verbose_name='课程')
    status = models.CharField('订单状态', max_length=20, choices=Status.choices, default=Status.PENDING, db_index=True)
    pay_method = models.CharField('支付方式', max_length=20, choices=PayMethod.choices, default=PayMethod.ALIPAY)
    trade_no = models.CharField('第三方交易号', max_length=120, blank=True)
    amount = models.DecimalField('实付金额', max_digits=10, decimal_places=2)
    refund_amount = models.DecimalField('退款金额', max_digits=10, decimal_places=2, default=0)
    platform_share_amount = models.DecimalField('平台分成金额', max_digits=10, decimal_places=2, default=0)
    teacher_share_amount = models.DecimalField('讲师分成金额', max_digits=10, decimal_places=2, default=0)
    paid_at = models.DateTimeField('支付时间', null=True, blank=True)
    refunded_at = models.DateTimeField('退款时间', null=True, blank=True)
    remark = models.CharField('备注', max_length=255, blank=True)

    class Meta:
        verbose_name = '订单'
        verbose_name_plural = '订单'
        ordering = ['-created_at']

    def __str__(self):
        return self.order_no


class RevenueRecord(TimeStampedModel):
    class Status(models.TextChoices):
        PENDING = 'pending', '待结算'
        SETTLED = 'settled', '已结算'
        WITHDRAWABLE = 'withdrawable', '可提现'

    teacher = models.ForeignKey(TeacherProfile, on_delete=models.PROTECT, related_name='revenues', verbose_name='讲师')
    course = models.ForeignKey(Course, on_delete=models.PROTECT, related_name='revenues', verbose_name='课程')
    order = models.OneToOneField(Order, on_delete=models.PROTECT, related_name='revenue_record', verbose_name='订单')
    gross_amount = models.DecimalField('订单总额', max_digits=10, decimal_places=2)
    teacher_amount = models.DecimalField('讲师收益', max_digits=10, decimal_places=2)
    platform_amount = models.DecimalField('平台收益', max_digits=10, decimal_places=2)
    teacher_share_rate = models.DecimalField('讲师分成比例', max_digits=5, decimal_places=2)
    platform_share_rate = models.DecimalField('平台分成比例', max_digits=5, decimal_places=2)
    status = models.CharField('结算状态', max_length=20, choices=Status.choices, default=Status.PENDING)
    settled_at = models.DateTimeField('结算时间', null=True, blank=True)

    class Meta:
        verbose_name = '收益记录'
        verbose_name_plural = '收益记录'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.teacher} - {self.teacher_amount}'


class Withdrawal(TimeStampedModel):
    class Status(models.TextChoices):
        PENDING = 'pending', '待审核'
        APPROVED = 'approved', '已通过'
        PAID = 'paid', '已打款'
        REJECTED = 'rejected', '已驳回'

    teacher = models.ForeignKey(TeacherProfile, on_delete=models.PROTECT, related_name='withdrawals', verbose_name='讲师')
    withdraw_no = models.CharField('提现单号', max_length=64, unique=True)
    amount = models.DecimalField('提现金额', max_digits=10, decimal_places=2)
    account_type = models.CharField('账户类型', max_length=30)
    account_name = models.CharField('账户名', max_length=100)
    account_no = models.CharField('账户号', max_length=120)
    bank_name = models.CharField('开户行', max_length=120, blank=True)
    status = models.CharField('审核状态', max_length=20, choices=Status.choices, default=Status.PENDING, db_index=True)
    audit_remark = models.TextField('审核备注', blank=True)
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='reviewed_withdrawals', verbose_name='审核人')
    reviewed_at = models.DateTimeField('审核时间', null=True, blank=True)
    paid_at = models.DateTimeField('打款时间', null=True, blank=True)

    class Meta:
        verbose_name = '提现'
        verbose_name_plural = '提现'
        ordering = ['-created_at']

    def __str__(self):
        return self.withdraw_no


class Comment(TimeStampedModel):
    class Status(models.TextChoices):
        PENDING = 'pending', '待审核'
        VISIBLE = 'visible', '显示'
        HIDDEN = 'hidden', '隐藏'
        REJECTED = 'rejected', '已驳回'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments', verbose_name='用户')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='comments', verbose_name='课程')
    content = models.TextField('评论内容')
    rating = models.PositiveSmallIntegerField('评分', default=5)
    status = models.CharField('审核状态', max_length=20, choices=Status.choices, default=Status.PENDING)
    audit_remark = models.CharField('审核备注', max_length=255, blank=True)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = '评论'
        ordering = ['-created_at']

    def __str__(self):
        return self.content[:30]


class Favorite(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites', verbose_name='用户')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='favorites', verbose_name='课程')

    class Meta:
        verbose_name = '收藏'
        verbose_name_plural = '收藏'
        unique_together = ('user', 'course')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user} 收藏 {self.course}'
