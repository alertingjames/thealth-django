# Generated by Django 3.0.4 on 2020-03-21 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=80)),
                ('password', models.CharField(max_length=30)),
                ('phone_number', models.CharField(max_length=30)),
                ('auth_status', models.CharField(max_length=30)),
                ('picture_url', models.CharField(max_length=1000)),
                ('address', models.CharField(max_length=200)),
                ('latitude', models.CharField(max_length=50)),
                ('longitude', models.CharField(max_length=50)),
                ('registered_time', models.CharField(max_length=50)),
                ('followings', models.CharField(max_length=11)),
                ('followers', models.CharField(max_length=11)),
                ('posts', models.CharField(max_length=11)),
                ('status', models.CharField(max_length=20)),
            ],
        ),
    ]
