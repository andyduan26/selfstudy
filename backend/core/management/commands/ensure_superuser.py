import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create or update the deployment superuser from environment variables.'

    def handle(self, *args, **options):
        username = os.getenv('DJANGO_SUPERUSER_USERNAME', '').strip()
        password = os.getenv('DJANGO_SUPERUSER_PASSWORD', '')
        email = os.getenv('DJANGO_SUPERUSER_EMAIL', '').strip()
        nickname = os.getenv('DJANGO_SUPERUSER_NICKNAME', '').strip()

        if not username or not password:
            self.stdout.write('DJANGO_SUPERUSER_USERNAME or DJANGO_SUPERUSER_PASSWORD is empty, skipped.')
            return

        User = get_user_model()
        user, created = User.objects.get_or_create(username=username)
        user.email = email
        user.nickname = nickname
        user.role = User.Role.ADMIN
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.set_password(password)
        user.save()

        action = 'created' if created else 'updated'
        self.stdout.write(self.style.SUCCESS(f'Superuser {username} {action}.'))
