# Generated by Django 4.0.2 on 2022-04-15 11:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0004_job_client_job'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='job',
        ),
        migrations.AddField(
            model_name='job',
            name='job',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, related_name='client', to='company.client'),
            preserve_default=False,
        ),
    ]
