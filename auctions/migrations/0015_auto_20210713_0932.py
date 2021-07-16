# Generated by Django 3.2.4 on 2021-07-13 09:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_remove_bid_initial_bid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.RemoveField(
            model_name='bid',
            name='title',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='title',
        ),
        migrations.AddField(
            model_name='auctionlisting',
            name='bids',
            field=models.ManyToManyField(blank=True, related_name='bids_in_auction', to='auctions.Bid'),
        ),
        migrations.AddField(
            model_name='auctionlisting',
            name='closed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='auctionlisting',
            name='comments',
            field=models.ManyToManyField(blank=True, related_name='comments_in_listing', to='auctions.Comment'),
        ),
        migrations.AddField(
            model_name='auctionlisting',
            name='last_bid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='last_bid_of_auction', to='auctions.bid'),
        ),
        migrations.AddField(
            model_name='auctionlisting',
            name='user',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, related_name='user_creating_the_listing', to='auctions.user'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bid',
            name='bid_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='bid',
            name='listing',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, related_name='bid_for_listing', to='auctions.auctionlisting'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bid',
            name='user',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, related_name='user_who_bids', to='auctions.user'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='comment',
            name='comment_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, related_name='user_who_comments', to='auctions.user'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='auctionlisting',
            name='created_on',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AlterField(
            model_name='comment',
            name='comment',
            field=models.TextField(),
        ),
        migrations.CreateModel(
            name='WatchList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('listing', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='watchlist_for_listing', to='auctions.auctionlisting')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users_watchlist', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='auctionlisting',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category_of_listing', to='auctions.category'),
        ),
    ]
