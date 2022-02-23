# Generated by Django 4.0.2 on 2022-02-20 09:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nameS', models.CharField(max_length=64)),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_%(app_label)s.%(class)s_set+', to='contenttypes.contenttype')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.IntegerField()),
                ('nameP', models.CharField(max_length=64)),
                ('brand', models.CharField(max_length=64)),
                ('size', models.IntegerField()),
                ('weight', models.IntegerField()),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('company_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='company.company')),
                ('address', models.IntegerField()),
                ('email', models.CharField(default=0, max_length=64)),
                ('contact', models.IntegerField()),
                ('zone', models.IntegerField()),
                ('location', models.CharField(max_length=64)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('company.company',),
        ),
        migrations.CreateModel(
            name='Personnel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nameC', models.CharField(max_length=64)),
                ('contact', models.IntegerField()),
                ('email', models.CharField(max_length=64)),
                ('company', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='personnel', to='company.company')),
            ],
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField()),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='productPrice', to='company.product')),
                ('supplier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='company.supplier')),
            ],
        ),
    ]
