from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class AuctionListing(models.Model):
    # Creating a model for the auction listings.
    title = models.CharField(max_length=64)
    description = models.TextField()
    current_price = models.ForeignKey('Bid', on_delete=models.CASCADE, related_name="listings", null=True)
    starting_bid = models.IntegerField()
    image = models.URLField(blank=True)
    comment = models.ManyToManyField("Comment", blank=True, related_name="listings")
    category = models.CharField(max_length=64, blank=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    watchlist = models.ManyToManyField(User, blank=True, related_name="watching")
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        """
        The __str__ function is a special function that is called when you use the print() function on
        an object
        :return: The title of the question
        """
        return f"{self.title}"

class Bid(models.Model):
    # Creating a bid model that has a bid and a bidder.
    bid = models.IntegerField()
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids", null=True)

    def __str__(self):
        """
        The __str__ function is a special function that is called when you print an object
        :return: The bid number
        """
        return f"{self.bid}"

class Comment(models.Model):
    # A Comment is a model that has an author and a message.
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    message = models.TextField()
    