from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


# Category Model Section
class Category(models.Model):
    name = models.CharField(max_length=50)

    @staticmethod
    def get_all_categories():
        return Category.objects.all()

    def __str__(self):
        return self.name


# Category Models Section
class Listing(models.Model):
    title = models.CharField(max_length=80)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    bid_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    imageurl = models.URLField(blank=True, max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    added_time = models.DateField("Added Time", auto_now_add=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    ended = models.BooleanField(default=False)
    winner = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True, related_name="winner")

    def __str__(self):
        return self.title

    @staticmethod
    def get_all_products():
        return Listing.objects.all()

    @staticmethod
    def get_all_product_by_category_id(category_id):
        if category_id:
            return Listing.objects.filter(category=category_id)
        else:
            return Listing.get_all_products()


# Models For Comment
class Comment(models.Model):
    comment = models.TextField()
    date = models.DateField("Added Date", auto_now_add=True)
    listing = models.ForeignKey('Listing', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.listing}->{self.user}"


# Model For Bid
class Bid(models.Model):
    value = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField("Added Date", auto_now_add=True)
    listing = models.ForeignKey('Listing', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.listing} -> {self.user}({self.value})"


# Model For WatchList
class Watchlist(models.Model):
    listing = models.ForeignKey('Listing', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.listing}->{self.user}"
