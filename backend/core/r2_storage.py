import mimetypes
from pathlib import Path

import boto3
from django.conf import settings


def is_r2_configured():
    return all([
        settings.R2_ACCOUNT_ID,
        settings.R2_ACCESS_KEY_ID,
        settings.R2_SECRET_ACCESS_KEY,
        settings.R2_BUCKET_NAME,
        settings.R2_PUBLIC_BASE_URL,
    ])


def upload_hls_directory_to_r2(video):
    if not is_r2_configured():
        return False, ''
    if not video.hls_path:
        return False, ''

    local_dir = settings.MEDIA_ROOT / video.hls_path
    if not local_dir.exists():
        return False, ''

    prefix = f'{settings.R2_HLS_PREFIX.strip("/")}/{video.id}'
    client = boto3.client(
        's3',
        endpoint_url=f'https://{settings.R2_ACCOUNT_ID}.r2.cloudflarestorage.com',
        aws_access_key_id=settings.R2_ACCESS_KEY_ID,
        aws_secret_access_key=settings.R2_SECRET_ACCESS_KEY,
        region_name='auto',
    )

    for path in local_dir.rglob('*'):
        if not path.is_file():
            continue
        relative_path = path.relative_to(local_dir).as_posix()
        object_key = f'{prefix}/{relative_path}'
        content_type = _content_type(path)
        client.upload_file(
            str(path),
            settings.R2_BUCKET_NAME,
            object_key,
            ExtraArgs={'ContentType': content_type},
        )

    base_url = settings.R2_PUBLIC_BASE_URL.rstrip('/')
    playlist_url = f'{base_url}/{prefix}/index.m3u8'
    video.hls_url = playlist_url
    video.save(update_fields=['hls_url', 'updated_at'])
    return True, playlist_url


def _content_type(path):
    if path.suffix == '.m3u8':
        return 'application/vnd.apple.mpegurl'
    if path.suffix == '.ts':
        return 'video/mp2t'
    return mimetypes.guess_type(Path(path).name)[0] or 'application/octet-stream'
