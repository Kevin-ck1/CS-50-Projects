# Generated by Django 3.1.4 on 2022-01-05 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='supplier',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]