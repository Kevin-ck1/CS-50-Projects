# Generated by Django 3.1.4 on 2021-04-01 15:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rfq', '0002_auto_20210331_2142'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='building',
            name='blocation',
        ),
    ]
