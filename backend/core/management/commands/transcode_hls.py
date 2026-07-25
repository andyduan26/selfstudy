from django.core.management.base import BaseCommand

from core.models import Video
from core.video_processing import transcode_video_to_hls


class Command(BaseCommand):
    help = '将上传的视频转码为 HLS 切片'

    def add_arguments(self, parser):
        parser.add_argument('--video-id', type=int, help='只转码指定视频 ID')
        parser.add_argument('--pending', action='store_true', help='只处理待转码视频')

    def handle(self, *args, **options):
        queryset = Video.objects.exclude(video_file='')
        if options.get('video_id'):
            queryset = queryset.filter(id=options['video_id'])
        if options.get('pending'):
            queryset = queryset.filter(transcode_status__in=['pending', 'failed'])

        total = queryset.count()
        if total == 0:
            self.stdout.write(self.style.WARNING('没有需要转码的视频'))
            return

        for video in queryset:
            ok, message = transcode_video_to_hls(video)
            if ok:
                self.stdout.write(self.style.SUCCESS(f'视频 {video.id} 转码完成：{message}'))
            else:
                self.stdout.write(self.style.ERROR(f'视频 {video.id} 转码失败：{message}'))
