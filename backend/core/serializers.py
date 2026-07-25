from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'nickname', 'email', 'phone', 'role', 'avatar', 'avatar_url', 'bio', 'is_verified_teacher')


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('id', 'username', 'nickname', 'email', 'password', 'role')
        extra_kwargs = {
            'username': {'required': False},
            'email': {'required': True},
            'nickname': {'required': True},
            'role': {'required': False},
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('该邮箱已注册')
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
        read_only_fields = ('status', 'audit_remark', 'reviewed_by', 'reviewed_at')


class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = '__all__'


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
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

    class Meta:
        model = Course
        fields = '__all__'


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
