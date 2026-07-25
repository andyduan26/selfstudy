from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_courseattachment'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='hls_path',
            field=models.CharField(blank=True, max_length=255, verbose_name='本地HLS目录'),
        ),
        migrations.AddField(
            model_name='video',
            name='hls_url',
            field=models.URLField(blank=True, verbose_name='HLS播放地址'),
        ),
        migrations.AlterField(
            model_name='video',
            name='source_type',
            field=models.CharField(choices=[('upload', '本地上传'), ('hls', 'HLS切片'), ('external', '外部地址'), ('vod', '云点播')], default='upload', max_length=20, verbose_name='视频来源'),
        ),
    ]
