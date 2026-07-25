import json

from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase

from core.models import Course, CourseAttachment, CourseCategory, TeacherApplication, TeacherProfile, User, Video


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

    def test_verified_teacher_can_upload_work_with_multiple_chapters(self):
        user = User.objects.create_user(
            username='teacher-chapters@example.com',
            email='teacher-chapters@example.com',
            phone='13800138004',
            password='StrongPass12345',
            role=User.Role.TEACHER,
            is_verified_teacher=True,
        )
        TeacherProfile.objects.create(user=user, real_name='章节老师', direction='前端开发')
        self.client.force_authenticate(user=user)

        response = self.client.post('/api/courses/upload-work/', {
            'title': '多章节上传课程',
            'category_name': '前端开发',
            'description': '这是一门包含多个章节视频的课程。',
            'price': '199.00',
            'chapters': json.dumps([
                {'title': '第一章 课程介绍', 'summary': '认识课程结构', 'videoTitle': '试看导学', 'isFreePreview': True, 'sortWeight': 1},
                {'title': '第二章 实战演示', 'summary': '完成项目案例', 'videoTitle': '核心实战', 'isFreePreview': False, 'sortWeight': 2},
            ]),
            'chapter_video_0': SimpleUploadedFile('intro.mp4', b'intro-video', content_type='video/mp4'),
            'chapter_video_1': SimpleUploadedFile('project.mp4', b'project-video', content_type='video/mp4'),
        }, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        course = Course.objects.get(title='多章节上传课程')
        self.assertEqual(course.chapters.count(), 2)
        self.assertEqual(Video.objects.filter(chapter__course=course).count(), 2)
        first_chapter = course.chapters.order_by('sort_weight').first()
        self.assertEqual(first_chapter.title, '第一章 课程介绍')
        self.assertTrue(first_chapter.is_free_preview)

    def test_verified_teacher_can_list_own_uploaded_works(self):
        user = User.objects.create_user(
            username='teacher-works@example.com',
            email='teacher-works@example.com',
            phone='13800138003',
            password='StrongPass12345',
            role=User.Role.TEACHER,
            is_verified_teacher=True,
        )
        teacher = TeacherProfile.objects.create(user=user, real_name='作品老师', direction='前端开发')
        category = CourseCategory.objects.create(name='前端开发', slug='frontend')
        Course.objects.create(
            teacher=teacher,
            category=category,
            title='我的待审核课程',
            description='课程说明',
            price='99.00',
            status=Course.Status.PENDING,
        )
        self.client.force_authenticate(user=user)

        response = self.client.get('/api/courses/my-works/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], '我的待审核课程')
        self.assertEqual(response.data[0]['status'], Course.Status.PENDING)

    def test_public_course_list_only_shows_approved_or_published_courses(self):
        user = User.objects.create_user(
            username='teacher-public@example.com',
            email='teacher-public@example.com',
            password='StrongPass12345',
            role=User.Role.TEACHER,
            is_verified_teacher=True,
        )
        teacher = TeacherProfile.objects.create(user=user, real_name='公开老师', direction='前端开发')
        category = CourseCategory.objects.create(name='前端开发', slug='frontend')
        Course.objects.create(
            teacher=teacher,
            category=category,
            title='待审核课程',
            status=Course.Status.PENDING,
        )
        Course.objects.create(
            teacher=teacher,
            category=category,
            title='已通过课程',
            status=Course.Status.APPROVED,
        )

        response = self.client.get('/api/courses/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [item['title'] for item in response.data['results']]
        self.assertEqual(titles, ['已通过课程'])
