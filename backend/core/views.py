from django.db import models
from django.db.models import Sum
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

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
from .serializers import (
    ChapterSerializer,
    CommentSerializer,
    CourseCategorySerializer,
    CourseSerializer,
    CustomTokenObtainPairSerializer,
    FavoriteSerializer,
    OrderSerializer,
    RegisterSerializer,
    RevenueRecordSerializer,
    TeacherApplicationSerializer,
    TeacherWorkUploadSerializer,
    TeacherProfileSerializer,
    UserSerializer,
    VideoSerializer,
    WithdrawalSerializer,
)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

    @action(detail=False, methods=['get', 'patch'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        if request.method == 'PATCH':
            serializer = self.get_serializer(request.user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        return Response(self.get_serializer(request.user).data)

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def register(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user, context={'request': request}).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=201)


class TeacherProfileViewSet(viewsets.ModelViewSet):
    queryset = TeacherProfile.objects.select_related('user').all()
    serializer_class = TeacherProfileSerializer
    permission_classes = [IsAdminOrReadOnly]


class TeacherApplicationViewSet(viewsets.ModelViewSet):
    queryset = TeacherApplication.objects.select_related('user', 'reviewed_by').all()
    serializer_class = TeacherApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

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
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action in ('list', 'retrieve') and not self.request.user.is_staff:
            return queryset.filter(status__in=[Course.Status.APPROVED, Course.Status.PUBLISHED])
        return queryset

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated], url_path='my-works')
    def my_works(self, request):
        queryset = Course.objects.select_related('teacher', 'category').prefetch_related('chapters__videos').filter(
            teacher__user=request.user,
        ).order_by('-updated_at')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAuthenticated], url_path='my-update')
    def my_update(self, request, pk=None):
        course = self.get_queryset().filter(pk=pk, teacher__user=request.user).first()
        if not course:
            return Response({'detail': '课程作品不存在或无权编辑'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(course, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(status=Course.Status.PENDING)
        return Response(serializer.data)

    @action(detail=True, methods=['delete'], permission_classes=[permissions.IsAuthenticated], url_path='my-delete')
    def my_delete(self, request, pk=None):
        course = Course.objects.filter(pk=pk, teacher__user=request.user).first()
        if not course:
            return Response({'detail': '课程作品不存在或无权删除'}, status=status.HTTP_404_NOT_FOUND)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated], url_path='upload-work')
    def upload_work(self, request):
        serializer = TeacherWorkUploadSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        category, _ = CourseCategory.objects.get_or_create(
            name=data['category_name'],
            defaults={'slug': data['category_name'].lower().replace(' ', '-')},
        )
        course = Course.objects.create(
            teacher=request.user.teacher_profile,
            category=category,
            title=data['title'],
            description=data.get('description', ''),
            price=data.get('price') or 0,
            cover=data.get('cover'),
            status=Course.Status.PENDING,
        )
        chapters_data = data.get('chapters_data') or []
        if chapters_data:
            for index, chapter_data in enumerate(chapters_data):
                chapter = Chapter.objects.create(
                    course=course,
                    title=chapter_data['title'],
                    summary=chapter_data.get('summary', ''),
                    sort_weight=chapter_data.get('sortWeight') or index + 1,
                    is_free_preview=bool(chapter_data.get('isFreePreview')),
                )
                video_file = request.FILES.get(f'chapter_video_{index}')
                if video_file:
                    Video.objects.create(
                        chapter=chapter,
                        title=chapter_data['videoTitle'],
                        video_file=video_file,
                        file_size=video_file.size,
                        sort_weight=chapter.sort_weight,
                        is_free_preview=bool(chapter_data.get('isFreePreview')),
                    )
        else:
            chapter = Chapter.objects.create(course=course, title='默认章节', sort_weight=1, is_free_preview=True)
            video_file = data.get('video_file')
            if video_file:
                Video.objects.create(
                    chapter=chapter,
                    title=f'{course.title} - 主视频',
                    video_file=video_file,
                    file_size=video_file.size,
                    is_free_preview=True,
                )
        attachment_file = data.get('attachment_file')
        if attachment_file:
            CourseAttachment.objects.create(
                course=course,
                title=attachment_file.name,
                file=attachment_file,
                file_size=attachment_file.size,
            )
        return Response(CourseSerializer(course, context={'request': request}).data, status=status.HTTP_201_CREATED)


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

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated], url_path='my-summary')
    def my_summary(self, request):
        teacher = getattr(request.user, 'teacher_profile', None)
        if not teacher:
            return Response({'detail': '只有认证讲师可以查看收益'}, status=status.HTTP_403_FORBIDDEN)

        queryset = self.get_queryset().filter(teacher=teacher)
        summary = queryset.aggregate(
            total=Sum('teacher_amount'),
            pending=Sum('teacher_amount', filter=models.Q(status=RevenueRecord.Status.PENDING)),
            withdrawable=Sum('teacher_amount', filter=models.Q(status=RevenueRecord.Status.WITHDRAWABLE)),
            settled=Sum('teacher_amount', filter=models.Q(status=RevenueRecord.Status.SETTLED)),
        )
        rows = RevenueRecordSerializer(queryset[:20], many=True, context={'request': request}).data
        return Response({
            'total': summary['total'] or 0,
            'pending': summary['pending'] or 0,
            'withdrawable': summary['withdrawable'] or 0,
            'settled': summary['settled'] or 0,
            'rows': rows,
        })


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
