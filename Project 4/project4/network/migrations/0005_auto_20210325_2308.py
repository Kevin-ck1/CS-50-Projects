# Generated by Django 3.1.4 on 2021-03-25 20:08

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_auto_20210323_2230'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='likers',
            field=models.ManyToManyField(related_name='post_likers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='like',
            name='liker',
        ),
        migrations.AddField(
            model_name='like',
            name='liker',
            field=models.ManyToManyField(related_name='post_liker', to=settings.AUTH_USER_MODEL),
        ),
    ]
