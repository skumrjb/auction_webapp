# Generated by Django 3.2.4 on 2021-07-12 10:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_alter_auctionlisting_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bid',
            old_name='starting_bid',
            new_name='title',
        ),
    ]
