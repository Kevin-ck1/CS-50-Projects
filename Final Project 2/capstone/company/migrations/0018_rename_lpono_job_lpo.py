# Generated by Django 4.0.6 on 2022-08-10 06:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0017_rename_deliveryno_job_lpono_remove_job_invoiceno_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='job',
            old_name='LPONo',
            new_name='lpo',
        ),
    ]
