# Generated by Django 3.1.4 on 2021-03-27 21:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_auto_20210325_2308'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='usermail',
            field=models.CharField(default=1, max_length=64),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comment',
            name='comment_item',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='post_comment', to='network.posts'),
        ),
    ]
