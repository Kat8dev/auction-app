from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver

class User(AbstractUser):
    pass

class Category(models.Model):
    category_name = models.CharField(max_length=64, unique=True) 
    objects = models.Manager()
    def __str__(self):
        return f"{self.category_name}"


class AuctionListing(models.Model):
    title = models.CharField(max_length=64)
    desc = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2) 
    image_url = models.URLField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, related_name="listings")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="won_listings", blank=True, null=True)
    objects = models.Manager()
    
    def __str__(self):
        return f"{self.title} by {self.created_by}"

class Bid(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    objects = models.Manager()
    
    def __str__(self):
        return f"{self.user} - {self.amount}"   

class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    objects = models.Manager()
    
    def __str__(self):
        return f"{self.user} - {self.content}"
    
class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    objects = models.Manager()
    
    def __str__(self):
        return f"{self.user} - {self.listing}"
    
    
@receiver(post_delete, sender=Watchlist)
def delete_bids_on_unwatch(sender, instance, **kwargs):
    """
    Automatically delete bids made by a user when they unwatch a listing.
    """
    if not instance.user or not instance.listing:
        return

    user = instance.user
    listing = instance.listing
    Bid.objects.filter(user=user, listing=listing).delete()
