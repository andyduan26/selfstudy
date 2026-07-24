from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

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
from .serializers import (
    ChapterSerializer,
    CommentSerializer,
    CourseCategorySerializer,
    CourseSerializer,
    FavoriteSerializer,
    OrderSerializer,
    RevenueRecordSerializer,
    TeacherApplicationSerializer,
    TeacherProfileSerializer,
    UserSerializer,
    VideoSerializer,
    WithdrawalSerializer,
)


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        return Response(self.get_serializer(request.user).data)


class TeacherProfileViewSet(viewsets.ModelViewSet):
    queryset = TeacherProfile.objects.select_related('user').all()
    serializer_class = TeacherProfileSerializer
    permission_classes = [IsAdminOrReadOnly]


class TeacherApplicationViewSet(viewsets.ModelViewSet):
    queryset = TeacherApplication.objects.select_related('user', 'reviewed_by').all()
    serializer_class = TeacherApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CourseCategoryViewSet(viewsets.ModelViewSet):
    queryset = CourseCategory.objects.all()
    serializer_class = CourseCategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.select_related('teacher', 'category').prefetch_related('chapters__videos').all()
    serializer_class = CourseSerializer
    permission_classes = [IsAdminOrReadOnly]


class ChapterViewSet(viewsets.ModelViewSet):
    queryset = Chapter.objects.select_related('course').prefetch_related('videos').all()
    serializer_class = ChapterSerializer
    permission_classes = [IsAdminOrReadOnly]


class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.select_related('chapter', 'chapter__course').all()
    serializer_class = VideoSerializer
    permission_classes = [IsAdminOrReadOnly]


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.select_related('user', 'course').all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]


class RevenueRecordViewSet(viewsets.ModelViewSet):
    queryset = RevenueRecord.objects.select_related('teacher', 'course', 'order').all()
    serializer_class = RevenueRecordSerializer
    permission_classes = [permissions.IsAdminUser]


class WithdrawalViewSet(viewsets.ModelViewSet):
    queryset = Withdrawal.objects.select_related('teacher', 'reviewed_by').all()
    serializer_class = WithdrawalSerializer
    permission_classes = [permissions.IsAuthenticated]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related('user', 'course').all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.select_related('user', 'course').all()
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
