from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.core.paginator import Paginator

from .models import User, Posts, Comment, Like, Profile


def index(request):
    #return render(request, "network/index.html")
    posts = Posts.objects.all()
    posts = posts.order_by("-dateTime").all()

    #paginating the posts
    paginator = Paginator(posts, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html",{
        "posts": page_obj,
    })


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

@csrf_exempt
def new(request):
    if request.method == "POST":
        data = json.loads(request.body)
        content = data.get("content", "")

        new_post = Posts(
            posterUsername = request.user,
            postContent = content,
            like = 0
        )
        new_post.save()
        return JsonResponse({"message": "Post create successfully."}, status=201)

def allPost(request):
    posts = Posts.objects.all()
    posts = posts.order_by("-dateTime").all()
    return JsonResponse([post.serialize() for post in posts], safe=False)
    print([post.serialize() for post in posts])
    
def profile(request, profilename):
    user = User.objects.get(username = profilename)
    profile = Profile.objects.get(user = user)

    followers = profile.follower.count()
    following = profile.following.count()

    try:
        profile.follower.get(username=request.user)
        button = "unFollow"
    except:
        button = "Follow" 
    
    posts = Posts.objects.filter(posterUsername = user)

    if request.method == "GET":
        return render(request, "network/index.html",{
        "profile" : profile,
        "followers": followers,
        "following": following,
        "posts": posts,
        "displaybutton":button
    })
    else:
        profile.follower.remove(username=request.user)

def following(request):
    user = request.user
    posts  = ""

    profile = Profile.objects.get(user = user)

    #Creating an empty queryset
    posts = Posts.objects.none()
    for person in profile.following.all():
        #To merge the various queryset
        posts = posts | Posts.objects.filter(posterUsername = person)
    return render(request, "network/index.html",{
        "posts": posts
    })

