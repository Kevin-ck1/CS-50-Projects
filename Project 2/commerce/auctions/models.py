from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    list_category = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.list_category}"

class AuctionListing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=64)
    desctiption = models.CharField(max_length=64)
    start_price = models.IntegerField()
    current_bid = models.IntegerField()
    photo = models.CharField(max_length=132, null = True, blank=True,)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing_creator")
    watchBidder = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, default=0, related_name="listing_watchBidder")
    Bidder = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, default=0, related_name="listing_Bidder")
    listing_category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, default=1, related_name="listing_category")
    listing_open = models.BooleanField(default=True) 
    
    def __str__(self):
        return f"{self.id}: {self.title}"

class Bid(models.Model):
    bid_item = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing_bidder")
    bid_price = models.IntegerField()
    
    def __str__(self):
        return f"{self.bid_item}"

class Comment(models.Model):
    comment = models.CharField(max_length=64)
    commentor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing_commentor")

    def __str__(self):
        return f"{self.comment}"

class Info(models.Model):
    won_listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    author_Username = models.CharField(max_length=64)
    author_Email = models.CharField(max_length=64)
    winner_Username = models.CharField(max_length=64)
    winner_Email = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.won_listing} {self.author_Username} {self.winner_Username}"



