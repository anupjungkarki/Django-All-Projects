from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("log-in", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("details/<str:title>", views.details, name="details"),
    path("listing", views.listing, name="listing"),
    path("create", views.create, name="create"),
    path("comment/<str:title>", views.comment, name="comment"),
    path("bid/<str:title>", views.bid, name="bid"),
    path("watchlist", views.view_watchlist, name="watchlist"),
    path("add-watchlist/<str:title>", views.add_to_watchlist, name="add-watchlist"),
    path("remove-watchlist/<str:title>", views.remove_from_watchlist, name="remove-watchlist"),
    path("ended/<str:title>", views.ended, name="ended")
]
