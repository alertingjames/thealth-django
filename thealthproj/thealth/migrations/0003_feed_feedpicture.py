# Generated by Django 3.0.4 on 2020-03-23 02:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('thealth', '0002_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('member_id', models.CharField(max_length=11)),
                ('picture_url', models.CharField(max_length=1000)),
                ('video_url', models.CharField(max_length=1000)),
                ('description', models.CharField(max_length=1000)),
                ('privacy', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=200)),
                ('latitude', models.CharField(max_length=50)),
                ('longitude', models.CharField(max_length=50)),
                ('posted_time', models.CharField(max_length=50)),
                ('likes', models.CharField(max_length=11)),
                ('comments', models.CharField(max_length=11)),
                ('is_liked', models.CharField(max_length=10)),
                ('is_saved', models.CharField(max_length=10)),
                ('status', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='FeedPicture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feed_id', models.CharField(max_length=11)),
                ('member_id', models.CharField(max_length=11)),
                ('picture_url', models.CharField(max_length=1000)),
            ],
        ),
    ]