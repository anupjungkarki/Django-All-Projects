from django.contrib import admin
from .models import Category, User, Listing, Comment, Bid, Watchlist

# Register your models here.
admin.site.register(Category)
admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Comment)
admin.site.register(Bid)
admin.site.register(Watchlist)
