from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    Chapter,
    Comment,
    Course,
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


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'phone', 'role', 'is_verified_teacher', 'is_active', 'date_joined')
    list_filter = ('role', 'is_verified_teacher', 'is_active', 'is_staff')
    search_fields = ('username', 'phone', 'email')
    ordering = ('-date_joined',)
    fieldsets = UserAdmin.fieldsets + (
        ('平台信息', {'fields': ('role', 'phone', 'avatar', 'bio', 'is_verified_teacher', 'sort_weight')}),
    )


@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'real_name', 'user', 'direction', 'revenue_share_rate', 'total_students', 'total_revenue', 'sort_weight')
    list_filter = ('direction',)
    search_fields = ('real_name', 'user__username', 'direction')
    ordering = ('-sort_weight', '-created_at')


@admin.register(TeacherApplication)
class TeacherApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'real_name', 'user', 'direction', 'status', 'reviewed_by', 'created_at')
    list_filter = ('status', 'direction')
    search_fields = ('real_name', 'phone', 'direction')
    ordering = ('-created_at',)


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
    list_display = ('id', 'title', 'teacher', 'category', 'status', 'price', 'view_count', 'sales_count', 'sort_weight')
    list_filter = ('status', 'category', 'level', 'is_free')
    search_fields = ('title', 'teacher__real_name')
    ordering = ('-sort_weight', '-created_at')
    inlines = [ChapterInline]


class VideoInline(admin.TabularInline):
    model = Video
    extra = 0


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'course', 'sort_weight', 'is_free_preview')
    list_filter = ('is_free_preview',)
    search_fields = ('title', 'course__title')
    inlines = [VideoInline]


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'chapter', 'duration_seconds', 'view_count', 'sort_weight', 'is_free_preview')
    list_filter = ('is_free_preview',)
    search_fields = ('title', 'chapter__title')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_no', 'user', 'course', 'status', 'amount', 'teacher_share_amount', 'platform_share_amount', 'created_at')
    list_filter = ('status',)
    search_fields = ('order_no', 'user__username', 'course__title')
    ordering = ('-created_at',)


@admin.register(RevenueRecord)
class RevenueRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'teacher', 'course', 'order', 'teacher_amount', 'platform_amount', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('teacher__real_name', 'course__title', 'order__order_no')


@admin.register(Withdrawal)
class WithdrawalAdmin(admin.ModelAdmin):
    list_display = ('id', 'withdraw_no', 'teacher', 'amount', 'account_type', 'status', 'reviewed_by', 'created_at')
    list_filter = ('status', 'account_type')
    search_fields = ('withdraw_no', 'teacher__real_name', 'account_name', 'account_no')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'course', 'rating', 'status', 'created_at')
    list_filter = ('status', 'rating')
    search_fields = ('user__username', 'course__title', 'content')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'course', 'created_at')
    search_fields = ('user__username', 'course__title')
