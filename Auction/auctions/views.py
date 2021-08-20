from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import ListingForm
from django.utils import timezone
from .models import Category, Comment, Listing, Bid, Watchlist
from django.contrib import messages

from .models import User


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def index(request):
    product = Listing.objects.filter(ended=False)
    return render(request, "auctions/index.html", {
        'listExist': True if len(product) != 0 else False,
        'products': product,
        'title': "Active Listings"
    })


def details(request, title):
    data = Listing.objects.get(title=title)
    cmt = Comment.objects.filter(listing=data.id)
    try:
        watch, own_listing, win = False, False, False
        for item in Watchlist.objects.filter(user=request.user):
            if item.listing.title == title:
                watch = True
        if request.user == data.user:
            own_listing = True
        if request.user == data.winner and data.ended:
            win = True
        return render(request, "auctions/product-details.html", {
            "products": data,
            "comments": cmt,
            "watch": watch,
            "own_listing": own_listing,
            "winner": win,
            "exist": False
        })
    except:
        return render(request, "auctions/product-details.html", {'products': data,
                                                                 'comments': cmt,
                                                                 "exist": False,
                                                                 "watch": watch
                                                                 })


def create(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = request.user
            data.added_time = timezone.now()
            data.save()
            return redirect("/")
        messages.success(request, "Successfully created the new Product!")
        return HttpResponseRedirect(reverse("create"))
    else:
        form = ListingForm()
        context = {'form': form}
        return render(request, "auctions/create.html", context)


def listing(request):
    products = None
    categories = Category.get_all_categories()
    categoryID = request.GET.get('category')
    if categoryID:
        products = Listing.get_all_product_by_category_id(categoryID)
    else:
        products = Listing.get_all_products()
    context = {'products': products, 'categories': categories}
    return render(request, "auctions/all-listing.html", context)


def comment(request, title):
    listing = Listing.objects.get(title=title)
    user = User.objects.filter(username=request.user)[0]
    comment = request.POST["comment"]
    context = Comment(listing=listing, user=user, comment=comment)
    context.save()
    return HttpResponseRedirect(reverse("index"))


def bid(request, title):
    data = Listing.objects.get(title=title)
    cmt = Comment.objects.filter(listing=data.id)
    amount = request.POST['bid-price']
    if float(data.price) < float(amount) and float(data.bid_price) < float(amount):
        data = Listing.objects.get(title=title)
        data.bid_price = amount
        data.winner = request.user
        data.save()
        context = Bid(value=amount, listing=data, user=request.user)
        context.save()
        messages.success(request, "Your Bid Is Successfully Completed !")
        return render(request, "auctions/product-details.html", {'products': data,
                                                                 'comments': cmt
                                                                 })
    else:
        messages.warning(request, "Your Bid Value Must Be Greater Than Current Value!")
        return render(request, "auctions/product-details.html", {'products': data,
                                                                 'comments': cmt
                                                                 })


def add_to_watchlist(request, title):
    data = Listing.objects.get(title=title)
    user = User.objects.filter(username=request.user)[0]
    context = Watchlist(user=user, listing=data)
    context.save()
    messages.success(request, "Successfully added new Product to watchlist!")
    return HttpResponseRedirect(reverse("watchlist"))


def view_watchlist(request):
    data = Watchlist.objects.filter(user=request.user)
    list = []
    for i in range(len(data)):
        list.append(Listing.objects.get(title=data[i].listing))
    return render(request, "auctions/watchlist.html",
                  {'list': data,
                   'is_exist': True if len(list) != 0 else False
                   })


def remove_from_watchlist(request, title):
    data = Listing.objects.get(title=title)
    user = User.objects.filter(username=request.user)[0]
    Watchlist.objects.filter(listing=data, user=user).delete()
    messages.error(request, "Successfully Removed Product From watchlist!")
    return HttpResponseRedirect(reverse("watchlist"))


def ended(request, title):
    data = Listing.objects.get(title=title)
    data.ended = True
    data.save()
    return HttpResponseRedirect(reverse("index"))
