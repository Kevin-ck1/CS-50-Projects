# Generated by Django 3.1.4 on 2021-12-22 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.IntegerField()),
                ('nameP', models.CharField(max_length=64)),
                ('brand', models.CharField(max_length=64)),
                ('price', models.IntegerField()),
                ('size', models.IntegerField()),
                ('weight', models.IntegerField()),
                ('description', models.TextField()),
            ],
        ),
    ]
