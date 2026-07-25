from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core.models import User


class AuthApiTests(APITestCase):
    def test_register_creates_user_and_returns_tokens(self):
        response = self.client.post('/api/users/register/', {
            'email': 'student@example.com',
            'nickname': '学习者',
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
