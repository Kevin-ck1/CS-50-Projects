# Generated by Django 3.1.4 on 2021-03-27 21:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0006_auto_20210328_0048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment_item',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='network.posts'),
        ),
    ]
