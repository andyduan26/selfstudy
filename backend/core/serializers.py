import json
import re

from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'nickname', 'email', 'phone', 'role', 'avatar', 'avatar_url', 'bio', 'is_verified_teacher', 'date_joined')
        read_only_fields = ('id', 'username', 'role', 'is_verified_teacher', 'date_joined')

    def validate_email(self, value):
        queryset = User.objects.filter(email=value)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        if value and queryset.exists():
            raise serializers.ValidationError('该邮箱已被使用')
        return value

    def validate_phone(self, value):
        if value and not re.fullmatch(r'1[3-9]\d{9}', value):
            raise serializers.ValidationError('请输入正确的中国大陆手机号')
        queryset = User.objects.filter(phone=value)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        if value and queryset.exists():
            raise serializers.ValidationError('该手机号已被使用')
        return value


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('id', 'username', 'nickname', 'email', 'phone', 'password', 'role')
        extra_kwargs = {
            'username': {'required': False},
            'email': {'required': True},
            'nickname': {'required': True},
            'phone': {'required': True},
            'role': {'required': False},
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('该邮箱已注册')
        return value

    def validate_phone(self, value):
        if not re.fullmatch(r'1[3-9]\d{9}', value):
            raise serializers.ValidationError('请输入正确的中国大陆手机号')
        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError('该手机号已注册')
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        email = validated_data['email']
        username = validated_data.pop('username', '') or email
        user = User(username=username, **validated_data)
        user.set_password(password)
        user.save()
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        identifier = attrs.get(self.username_field)
        if identifier:
            user = (
                User.objects.filter(username=identifier).first()
                or User.objects.filter(email=identifier).first()
                or User.objects.filter(phone=identifier).first()
                or User.objects.filter(nickname=identifier).first()
            )
            if user:
                attrs[self.username_field] = user.username
        data = super().validate(attrs)
        data['user'] = UserSerializer(self.user, context=self.context).data
        return data


class TeacherProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = TeacherProfile
        fields = '__all__'


class TeacherApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherApplication
        fields = '__all__'
        read_only_fields = ('user', 'status', 'audit_remark', 'reviewed_by', 'reviewed_at')


class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = '__all__'


class VideoSerializer(serializers.ModelSerializer):
    hls_url = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = '__all__'

    def get_hls_url(self, obj):
        if not obj.hls_url:
            return ''
        if obj.hls_url.startswith('/media/courses/hls/') and settings.R2_PUBLIC_BASE_URL:
            return f'{settings.R2_PUBLIC_BASE_URL.rstrip("/")}/{obj.hls_url.removeprefix("/media/")}'
        return obj.hls_url


class CourseAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseAttachment
        fields = '__all__'


class ChapterSerializer(serializers.ModelSerializer):
    videos = VideoSerializer(many=True, read_only=True)

    class Meta:
        model = Chapter
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    teacher_detail = TeacherProfileSerializer(source='teacher', read_only=True)
    category_detail = CourseCategorySerializer(source='category', read_only=True)
    chapters = ChapterSerializer(many=True, read_only=True)
    attachments = CourseAttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'


class TeacherWorkUploadSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=150)
    category_name = serializers.CharField(max_length=50)
    description = serializers.CharField(required=False, allow_blank=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    cover = serializers.ImageField(required=False)
    video_file = serializers.FileField(required=False)
    attachment_file = serializers.FileField(required=False)
    chapters = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs):
        user = self.context['request'].user
        if not getattr(user, 'is_verified_teacher', False) or not hasattr(user, 'teacher_profile'):
            raise serializers.ValidationError('只有认证讲师可以上传作品')
        raw_chapters = attrs.get('chapters')
        if raw_chapters:
            try:
                chapters = json.loads(raw_chapters)
            except json.JSONDecodeError as exc:
                raise serializers.ValidationError({'chapters': '章节数据格式不正确'}) from exc
            if not isinstance(chapters, list) or not chapters:
                raise serializers.ValidationError({'chapters': '请至少添加一个课程章节'})
            for index, chapter in enumerate(chapters, start=1):
                if not isinstance(chapter, dict):
                    raise serializers.ValidationError({'chapters': f'第 {index} 个章节格式不正确'})
                if not chapter.get('title'):
                    raise serializers.ValidationError({'chapters': f'第 {index} 个章标题不能为空'})
                lessons = chapter.get('lessons')
                if lessons is not None:
                    if not isinstance(lessons, list) or not lessons:
                        raise serializers.ValidationError({'chapters': f'第 {index} 章请至少添加一个节'})
                    for lesson_index, lesson in enumerate(lessons, start=1):
                        if not isinstance(lesson, dict):
                            raise serializers.ValidationError({'chapters': f'第 {index} 章第 {lesson_index} 节格式不正确'})
                        if not lesson.get('title'):
                            raise serializers.ValidationError({'chapters': f'第 {index} 章第 {lesson_index} 节标题不能为空'})
                elif not chapter.get('videoTitle'):
                    raise serializers.ValidationError({'chapters': f'第 {index} 个视频标题不能为空'})
            attrs['chapters_data'] = chapters
        return attrs


class OrderSerializer(serializers.ModelSerializer):
    course_detail = CourseSerializer(source='course', read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = (
            'order_no',
            'user',
            'status',
            'trade_no',
            'amount',
            'refund_amount',
            'platform_share_amount',
            'teacher_share_amount',
            'paid_at',
            'refunded_at',
        )


class RevenueRecordSerializer(serializers.ModelSerializer):
    course_detail = CourseSerializer(source='course', read_only=True)

    class Meta:
        model = RevenueRecord
        fields = '__all__'


class WithdrawalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Withdrawal
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    user_detail = UserSerializer(source='user', read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('user', 'status', 'audit_remark')


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'
