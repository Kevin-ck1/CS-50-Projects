# Generated by Django 3.1.4 on 2021-04-01 16:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rfq', '0003_remove_building_blocation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='building1',
        ),
        migrations.DeleteModel(
            name='Building',
        ),
    ]