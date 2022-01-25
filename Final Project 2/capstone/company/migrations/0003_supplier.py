# Generated by Django 3.1.4 on 2022-01-25 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0002_product_supplier'),
    ]

    operations = [
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nameS', models.CharField(max_length=64)),
                ('address', models.IntegerField()),
                ('contact', models.IntegerField()),
                ('zone', models.IntegerField()),
                ('location', models.CharField(max_length=64)),
            ],
        ),
    ]
