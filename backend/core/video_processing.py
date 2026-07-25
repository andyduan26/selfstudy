import shutil
import subprocess
from pathlib import Path

from django.conf import settings

from .models import Video


def transcode_video_to_hls(video):
    if not video.video_file:
        return False, '没有原始视频文件'
    if not shutil.which('ffmpeg'):
        video.transcode_status = 'failed'
        video.save(update_fields=['transcode_status', 'updated_at'])
        return False, '未安装 ffmpeg'

    source_path = Path(video.video_file.path)
    output_dir = settings.MEDIA_ROOT / 'courses' / 'hls' / str(video.id)
    output_dir.mkdir(parents=True, exist_ok=True)
    playlist_path = output_dir / 'index.m3u8'

    command = [
        'ffmpeg',
        '-y',
        '-i',
        str(source_path),
        '-c:v',
        'libx264',
        '-preset',
        'veryfast',
        '-crf',
        '23',
        '-c:a',
        'aac',
        '-b:a',
        '128k',
        '-hls_time',
        '8',
        '-hls_playlist_type',
        'vod',
        '-hls_segment_filename',
        str(output_dir / 'segment_%03d.ts'),
        str(playlist_path),
    ]

    video.transcode_status = 'processing'
    video.save(update_fields=['transcode_status', 'updated_at'])
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        video.transcode_status = 'failed'
        video.save(update_fields=['transcode_status', 'updated_at'])
        return False, result.stderr[-500:] or 'ffmpeg 转码失败'

    relative_playlist = playlist_path.relative_to(settings.MEDIA_ROOT)
    video.source_type = Video.SourceType.HLS
    video.hls_path = str(output_dir.relative_to(settings.MEDIA_ROOT))
    video.hls_url = f'{settings.MEDIA_URL}{relative_playlist}'.replace('\\', '/')
    video.transcode_status = 'completed'
    video.save(update_fields=['source_type', 'hls_path', 'hls_url', 'transcode_status', 'updated_at'])
    return True, video.hls_url
