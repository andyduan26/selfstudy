import mimetypes

import boto3
from django.conf import settings
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible


@deconstructible
class R2MediaStorage(Storage):
    def __init__(self):
        self.client = boto3.client(
            's3',
            endpoint_url=f'https://{settings.R2_ACCOUNT_ID}.r2.cloudflarestorage.com',
            aws_access_key_id=settings.R2_ACCESS_KEY_ID,
            aws_secret_access_key=settings.R2_SECRET_ACCESS_KEY,
            region_name='auto',
        )

    def _save(self, name, content):
        content.seek(0)
        self.client.upload_fileobj(
            content,
            settings.R2_BUCKET_NAME,
            name,
            ExtraArgs={'ContentType': self._content_type(name)},
        )
        return name

    def exists(self, name):
        try:
            self.client.head_object(Bucket=settings.R2_BUCKET_NAME, Key=name)
            return True
        except Exception:
            return False

    def url(self, name):
        return f'{settings.R2_PUBLIC_BASE_URL.rstrip("/")}/{name.lstrip("/")}'

    def _content_type(self, name):
        if name.endswith('.m3u8'):
            return 'application/vnd.apple.mpegurl'
        if name.endswith('.ts'):
            return 'video/mp2t'
        return mimetypes.guess_type(name)[0] or 'application/octet-stream'
