from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core.models import User


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
