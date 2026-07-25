from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase

from core.models import Course, CourseAttachment, TeacherApplication, TeacherProfile, User, Video


class AuthApiTests(APITestCase):
    def test_register_creates_user_and_returns_tokens(self):
        response = self.client.post('/api/users/register/', {
            'email': 'student@example.com',
            'nickname': '学习者',
            'phone': '13800138000',
            'password': 'StrongPass12345',
            'role': User.Role.USER,
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='student@example.com', nickname='学习者').exists())
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_token_login_returns_user_profile(self):
        User.objects.create_user(
            username='teacher@example.com',
            email='teacher@example.com',
            phone='13900139000',
            password='StrongPass12345',
            nickname='讲师',
            role=User.Role.TEACHER,
        )

        response = self.client.post(reverse('token_obtain_pair'), {
            'username': 'teacher@example.com',
            'password': 'StrongPass12345',
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['role'], User.Role.TEACHER)
        self.assertIn('access', response.data)

        phone_response = self.client.post(reverse('token_obtain_pair'), {
            'username': '13900139000',
            'password': 'StrongPass12345',
        }, format='json')
        self.assertEqual(phone_response.status_code, status.HTTP_200_OK)

        nickname_response = self.client.post(reverse('token_obtain_pair'), {
            'username': '讲师',
            'password': 'StrongPass12345',
        }, format='json')
        self.assertEqual(nickname_response.status_code, status.HTTP_200_OK)

    def test_user_can_update_own_profile(self):
        register_response = self.client.post('/api/users/register/', {
            'email': 'profile@example.com',
            'nickname': '旧昵称',
            'phone': '13700137000',
            'password': 'StrongPass12345',
            'role': User.Role.USER,
        }, format='json')
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {register_response.data['access']}")

        response = self.client.patch('/api/users/me/', {
            'nickname': '新昵称',
            'bio': '正在学习 Vue 和 Django',
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nickname'], '新昵称')


class TeacherWorkflowTests(APITestCase):
    def test_user_can_submit_teacher_application(self):
        user = User.objects.create_user(
            username='apply@example.com',
            email='apply@example.com',
            phone='13800138001',
            password='StrongPass12345',
        )
        self.client.force_authenticate(user=user)

        response = self.client.post('/api/teacher-applications/', {
            'real_name': '申请老师',
            'phone': '13800138001',
            'direction': '前端开发',
            'experience': '我有多年项目和教学经验，擅长 Vue 和 Django。',
            'portfolio_url': 'https://example.com/work',
            'sample_video': SimpleUploadedFile('sample.mp4', b'video-bytes', content_type='video/mp4'),
            'certificate_file': SimpleUploadedFile('cert.pdf', b'pdf-bytes', content_type='application/pdf'),
        }, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(TeacherApplication.objects.filter(user=user, real_name='申请老师').exists())

    def test_verified_teacher_can_upload_work_with_files(self):
        user = User.objects.create_user(
            username='teacher-upload@example.com',
            email='teacher-upload@example.com',
            phone='13800138002',
            password='StrongPass12345',
            role=User.Role.TEACHER,
            is_verified_teacher=True,
        )
        TeacherProfile.objects.create(user=user, real_name='上传老师', direction='前端开发')
        self.client.force_authenticate(user=user)

        response = self.client.post('/api/courses/upload-work/', {
            'title': '真实上传课程',
            'category_name': '前端开发',
            'description': '这是一门用于测试上传链路的课程说明。',
            'price': '99.00',
            'video_file': SimpleUploadedFile('lesson.mp4', b'video-bytes', content_type='video/mp4'),
            'attachment_file': SimpleUploadedFile('material.zip', b'zip-bytes', content_type='application/zip'),
        }, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        course = Course.objects.get(title='真实上传课程')
        self.assertEqual(course.status, Course.Status.PENDING)
        self.assertTrue(Video.objects.filter(chapter__course=course).exists())
        self.assertTrue(CourseAttachment.objects.filter(course=course).exists())
