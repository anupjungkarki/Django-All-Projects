# Generated by Django 3.0.7 on 2020-08-16 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_listing_entry'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='entry',
        ),
        migrations.AddField(
            model_name='listing',
            name='bid_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
            preserve_default=False,
        ),
    ]
