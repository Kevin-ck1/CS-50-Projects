# Generated by Django 4.0.2 on 2022-03-04 14:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0002_alter_company_id_alter_personnel_id_alter_price_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('company_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='company.company')),
                ('county', models.IntegerField()),
                ('location', models.CharField(max_length=64)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('company.company',),
        ),
        migrations.RemoveField(
            model_name='supplier',
            name='address',
        ),
        migrations.RemoveField(
            model_name='supplier',
            name='contact',
        ),
        migrations.RemoveField(
            model_name='supplier',
            name='email',
        ),
        migrations.AddField(
            model_name='company',
            name='address',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='company',
            name='contact',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='company',
            name='email',
            field=models.CharField(default=0, max_length=64),
        ),
    ]
