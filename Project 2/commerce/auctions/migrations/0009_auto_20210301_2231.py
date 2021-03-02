# Generated by Django 3.1.4 on 2021-03-01 19:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_auto_20210301_2220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='listing_category',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, related_name='item_category', to='auctions.category'),
        ),
    ]