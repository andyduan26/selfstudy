from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    ChapterViewSet,
    CommentViewSet,
    CourseCategoryViewSet,
    CourseViewSet,
    FavoriteViewSet,
    OrderViewSet,
    RevenueRecordViewSet,
    TeacherApplicationViewSet,
    TeacherProfileViewSet,
    UserViewSet,
    VideoViewSet,
    WithdrawalViewSet,
)

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('teacher-profiles', TeacherProfileViewSet)
router.register('teacher-applications', TeacherApplicationViewSet)
router.register('categories', CourseCategoryViewSet)
router.register('courses', CourseViewSet)
router.register('chapters', ChapterViewSet)
router.register('videos', VideoViewSet)
router.register('orders', OrderViewSet)
router.register('revenues', RevenueRecordViewSet)
router.register('withdrawals', WithdrawalViewSet)
router.register('comments', CommentViewSet)
router.register('favorites', FavoriteViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
