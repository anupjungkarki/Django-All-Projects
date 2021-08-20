from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("following/<str:username>", views.following, name="following"),
    path("newpost/<str:username>", views.add_post, name="newpost"),
    path("edit/<int:post_id>", views.edit, name="edit"),
    path("delete/<int:post_id>", views.delete, name="delete"),
    path("like_post/", views.like_post, name="like_post")
]
