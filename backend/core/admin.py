from django.contrib import admin
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.admin import UserAdmin
from django.core.mail import send_mail
from django.utils import timezone

from .models import (
    Chapter,
    Comment,
    Course,
    CourseAttachment,
    CourseCategory,
    Favorite,
    Order,
    RevenueRecord,
    TeacherApplication,
    TeacherProfile,
    User,
    Video,
    Withdrawal,
)


def notify_teacher_application(application, subject, message):
    if application.user.email:
        send_mail(subject, message, None, [application.user.email], fail_silently=settings.EMAIL_FAIL_SILENTLY)


def format_datetime(value):
    if not value:
        return '-'
    return timezone.localtime(value).strftime('%Y年%m月%d日 %H:%M')


def user_display_name(user):
    return user.nickname or user.username


def build_teacher_approved_message(application):
    user = application.user
    return f"""尊敬的 {user_display_name(user)}：

您好！

恭喜您，您提交的“我要自学网”讲师认证申请已审核通过。感谢您愿意将专业知识与学习者分享，平台已为您开通认证讲师身份。

账号信息：
昵称：{user_display_name(user)}
账号：{user.username}
注册时间：{format_datetime(user.date_joined)}
认证方向：{application.direction}
审核时间：{format_datetime(application.reviewed_at)}

您现在可以登录平台进入个人中心，上传课程作品、填写课程说明，并管理后续内容。

感谢您对我要自学网的信任与支持。期待您的课程帮助更多学习者系统成长。

我要自学网运营团队
{format_datetime(timezone.now())}
"""


def build_teacher_rejected_message(application):
    user = application.user
    return f"""尊敬的 {user_display_name(user)}：

您好！

感谢您提交“我要自学网”讲师认证申请。很遗憾，本次资料暂未通过审核。

账号信息：
昵称：{user_display_name(user)}
账号：{user.username}
注册时间：{format_datetime(user.date_joined)}
申请方向：{application.direction}
审核时间：{format_datetime(application.reviewed_at)}

审核备注：
{application.audit_remark}

您可以根据审核备注补充或修正资料后再次提交申请。感谢您的理解与支持。

我要自学网运营团队
{format_datetime(timezone.now())}
"""


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'nickname', 'phone', 'role', 'is_verified_teacher', 'is_active', 'date_joined')
    list_filter = ('role', 'is_verified_teacher', 'is_active', 'is_staff')
    search_fields = ('username', 'nickname', 'phone', 'email')
    ordering = ('-date_joined',)
    fieldsets = UserAdmin.fieldsets + (
        ('平台信息', {'fields': ('role', 'nickname', 'phone', 'avatar', 'avatar_url', 'bio', 'is_verified_teacher', 'sort_weight')}),
    )


@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'real_name', 'user', 'direction', 'revenue_share_rate', 'total_students', 'total_revenue', 'sort_weight')
    list_filter = ('direction',)
    search_fields = ('real_name', 'user__username', 'direction')
    ordering = ('-sort_weight', '-created_at')


@admin.register(TeacherApplication)
class TeacherApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'real_name', 'user', 'direction', 'status', 'sample_video', 'reviewed_by', 'created_at')
    list_filter = ('status', 'direction')
    search_fields = ('real_name', 'phone', 'direction')
    ordering = ('-created_at',)
    actions = ('approve_applications', 'reject_applications')

    @admin.action(description='审核通过并开通讲师')
    def approve_applications(self, request, queryset):
        count = 0
        for application in queryset:
            application.status = TeacherApplication.Status.APPROVED
            application.reviewed_by = request.user
            application.reviewed_at = timezone.now()
            application.audit_remark = application.audit_remark or '审核通过，已开通讲师身份。'
            application.save()

            user = application.user
            user.role = User.Role.TEACHER
            user.is_verified_teacher = True
            user.phone = user.phone or application.phone
            user.save(update_fields=['role', 'is_verified_teacher', 'phone'])

            TeacherProfile.objects.get_or_create(
                user=user,
                defaults={
                    'real_name': application.real_name,
                    'direction': application.direction,
                    'experience': application.experience,
                    'intro': application.experience,
                },
            )
            notify_teacher_application(
                application,
                '我要自学网讲师认证审核通过',
                build_teacher_approved_message(application),
            )
            count += 1
        self.message_user(request, f'已通过 {count} 个讲师申请，并发送邮件通知。', messages.SUCCESS)

    @admin.action(description='驳回讲师申请并邮件通知')
    def reject_applications(self, request, queryset):
        count = 0
        for application in queryset:
            application.status = TeacherApplication.Status.REJECTED
            application.reviewed_by = request.user
            application.reviewed_at = timezone.now()
            application.audit_remark = application.audit_remark or '资料暂未通过审核，请补充后重新提交。'
            application.save()
            notify_teacher_application(
                application,
                '我要自学网讲师认证审核结果',
                build_teacher_rejected_message(application),
            )
            count += 1
        self.message_user(request, f'已驳回 {count} 个讲师申请，并发送邮件通知。', messages.WARNING)


@admin.register(CourseCategory)
class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'sort_weight', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'slug')
    ordering = ('-sort_weight', 'id')


class ChapterInline(admin.TabularInline):
    model = Chapter
    extra = 0


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'teacher', 'category', 'status', 'price', 'cover', 'view_count', 'sales_count', 'sort_weight')
    list_filter = ('status', 'category', 'level', 'is_free')
    search_fields = ('title', 'teacher__real_name')
    ordering = ('-sort_weight', '-created_at')
    inlines = [ChapterInline]


class VideoInline(admin.TabularInline):
    model = Video
    extra = 0


class CourseAttachmentInline(admin.TabularInline):
    model = CourseAttachment
    extra = 0


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'course', 'sort_weight', 'is_free_preview')
    list_filter = ('is_free_preview',)
    search_fields = ('title', 'course__title')
    inlines = [VideoInline]


@admin.register(CourseAttachment)
class CourseAttachmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'course', 'file_type', 'file_size', 'sort_weight', 'created_at')
    list_filter = ('file_type',)
    search_fields = ('title', 'course__title')


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'chapter', 'source_type', 'video_file', 'video_url', 'vod_file_id', 'transcode_status', 'duration_seconds', 'view_count', 'is_free_preview')
    list_filter = ('source_type', 'transcode_status', 'is_free_preview')
    search_fields = ('title', 'chapter__title')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_no', 'user', 'course', 'status', 'pay_method', 'amount', 'refund_amount', 'teacher_share_amount', 'platform_share_amount', 'created_at')
    list_filter = ('status', 'pay_method')
    search_fields = ('order_no', 'trade_no', 'user__username', 'course__title')
    ordering = ('-created_at',)


@admin.register(RevenueRecord)
class RevenueRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'teacher', 'course', 'order', 'teacher_amount', 'platform_amount', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('teacher__real_name', 'course__title', 'order__order_no')


@admin.register(Withdrawal)
class WithdrawalAdmin(admin.ModelAdmin):
    list_display = ('id', 'withdraw_no', 'teacher', 'amount', 'account_type', 'bank_name', 'status', 'reviewed_by', 'created_at')
    list_filter = ('status', 'account_type')
    search_fields = ('withdraw_no', 'teacher__real_name', 'account_name', 'account_no')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'course', 'rating', 'status', 'audit_remark', 'created_at')
    list_filter = ('status', 'rating')
    search_fields = ('user__username', 'course__title', 'content')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'course', 'created_at')
    search_fields = ('user__username', 'course__title')
