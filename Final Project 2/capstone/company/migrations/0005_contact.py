# Generated by Django 3.1.4 on 2022-01-26 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0004_supplier_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nameC', models.CharField(max_length=64)),
                ('contact', models.IntegerField()),
                ('email', models.CharField(max_length=64)),
            ],
        ),
    ]
