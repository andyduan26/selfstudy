import re

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
    class Meta:
        model = Video
        fields = '__all__'


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

    def validate(self, attrs):
        user = self.context['request'].user
        if not getattr(user, 'is_verified_teacher', False) or not hasattr(user, 'teacher_profile'):
            raise serializers.ValidationError('只有认证讲师可以上传作品')
        return attrs


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class RevenueRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = RevenueRecord
        fields = '__all__'


class WithdrawalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Withdrawal
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'
