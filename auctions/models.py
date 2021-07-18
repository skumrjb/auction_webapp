from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime
from django.utils import timezone


class User(AbstractUser):
    pass

class AuctionListing(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='user_creating_the_listing')
    category = models.CharField(max_length=64)
    # Auction Listing details
    title = models.CharField(max_length=64)
    img= models.URLField(blank=True, default='')
    description = models.TextField(max_length=1024)
    # Bid - Starting, number of bids, Final bid
    starting_bid = models.IntegerField()
    bids = models.ManyToManyField('Bid', related_name='bids_in_auction', blank=True)
    last_bid = models.ForeignKey('Bid', on_delete=models.CASCADE, related_name='last_bid_of_auction', blank=True, null=True)
    #Comments
    comments = models.ManyToManyField('Comment', related_name='comments_in_listing', blank=True)
    # Auction Listing creation date
    created_on = models.DateTimeField(default=timezone.now, editable=False)
    # Status
    closed = models.BooleanField(default=False)

    def auction_publish(self):
        return self.created_on.strftime('%B %d %Y')
    
    def __str__(self):
        return f'{self.title}'

class Bid(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='user_who_bids')
    listing = models.ForeignKey('AuctionListing', on_delete=models.CASCADE, related_name='bid_for_listing')
    bid_price = models.IntegerField(blank=False)
    bid_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f'{self.bid_price}'

class Comment(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='user_who_comments')
    comment = models.TextField()
    comment_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f'{self.user}: {self.comment}'

class WatchList(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='users_watchlist')
    listing = models.ManyToManyField('AuctionListing', related_name='watchlist_for_listing', blank=True)

    def __str__(self):
        return f'Personal watchlist of {self.user}'