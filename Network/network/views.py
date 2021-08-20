from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import JsonResponse
from .models import User, Post, Like, Profile


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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def index(request):
    content = Post.objects.all().order_by('id').reverse()
    user = request.user
    paginator = Paginator(content, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'posts': content, 'user': user, 'pages': page_obj}
    return render(request, "network/index.html", context)


def add_post(request, username):
    if request.method == 'POST':
        user = get_object_or_404(User, username=username)
        textarea = request.POST['textarea']
        if not textarea:
            return HttpResponseRedirect(reverse("index"))
        post = Post.objects.create(content=textarea, user=user)
        post.save()
        return redirect('/')


def following(request, username):
    if request.method == 'GET':
        current_user = get_object_or_404(User, username=username)
        follows = Profile.objects.filter(follower=current_user)
        posts = Post.objects.all().order_by('id').reverse()
        posted = []
        for p in posts:
            for follower in follows:
                if follower.target == p.user:
                    posted.append(p)
        if not follows:
            return render(request, 'network/following.html', {'message': "You Haven't Follow Anybody Yet!!"})
        paginator = Paginator(posted, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, "network/following.html", {'pages': page_obj})


def profile(request, username):
    if request.method == 'GET':
        current_user = request.user
        profile_user = get_object_or_404(User, username=username)
        posts = Post.objects.filter(user=profile_user).order_by('id').reverse()
        follower = Profile.objects.filter(target=profile_user)
        following = Profile.objects.filter(follower=profile_user)
        if request.user.is_anonymous:
            return redirect('login')
        else:
            following_each_other = Profile.objects.filter(follower=current_user, target=profile_user)
            total_follower = len(follower)
            total_following = len(following)
            paginator = Paginator(posts, 4)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            context = {'posts': posts.count(),
                       'profile_user': profile_user,
                       'pages': page_obj,
                       'follower': follower,
                       'total_follower': total_follower,
                       'following': following,
                       'total_following': total_following,
                       'following_each_other': following_each_other
                       }
            return render(request, "network/profile.html", context)
    else:
        current_user = request.user
        profile_user = get_object_or_404(User, username=username)
        posts = Post.objects.filter(user=profile_user).order_by('id').reverse()
        following_each_other = Profile.objects.filter(follower=request.user, target=profile_user)
        paginator = Paginator(posts, 1)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        if not following_each_other:
            follow = Profile.objects.create(target=profile_user, follower=current_user)
            follow.save()
            follower = Profile.objects.filter(target=profile_user)
            following = Profile.objects.filter(follower=profile_user)
            following_each_other = Profile.objects.filter(follower=request.user, target=profile_user)
            total_follower = len(follower)
            total_following = len(following)
            context = {'posts': posts.count(),
                       'profile_user': profile_user,
                       'pages': page_obj,
                       'follower': follower,
                       'following': following,
                       'total_following': total_following,
                       'total_follower': total_follower,
                       'following_each_other': following_each_other
                       }
            return render(request, "network/profile.html", context)
        else:
            following_each_other.delete()
            follower = Profile.objects.filter(target=profile_user)
            following = Profile.objects.filter(follower=profile_user)
            total_follower = len(follower)
            total_following = len(following)
            context = {'posts': posts.count(),
                       'profile_user': profile_user,
                       'pages': page_obj,
                       'follower': follower,
                       'following': following,
                       'total_following': total_following,
                       'total_follower': total_follower,
                       'following_each_other': following_each_other
                       }
            return render(request, "network/profile.html", context)


def edit(request, post_id):
    if request.method == 'POST':
        post = Post.objects.get(pk=post_id)
        textarea = request.POST['textarea']
        post.content = textarea
        post.save()
        return redirect('/')


def delete(request, post_id):
    post = Post.objects.get(pk=post_id)
    if request.method == 'POST':
        post.delete()
    return redirect('/')


def like_post(request):
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)
        if user in post_obj.liked.all():
            post_obj.liked.remove(user)
        else:
            post_obj.liked.add(user)
        like, created = Like.objects.get_or_create(user=user, post_id=post_id)
        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'
                post_obj.save()
                like.save()
        # data = {
        #     'value': like.value,
        #     'likes': post_obj.liked.all().count()
        # }
    return redirect('following', username=user)
