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
from django.contrib.auth.decorators import login_required

from .models import User, Posts, Comment, Like, Profile


def index(request):
    #return render(request, "network/index.html")
    posts = Posts.objects.all()
    posts = posts.order_by("-dateTime").all()

    #paginating the posts
    paginator = Paginator(posts, 10)
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
            #Creating a Profile for a user once registered
            profile = Profile(user = user, usermail=email)
            profile.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required(login_url="login")
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
    posts = posts.order_by("-dateTime").all()
    #paginating the posts
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    
    return render(request, "network/index.html",{
        "profile" : profile,
        "followers": followers,
        "following": following,
        "posts": page_obj,
        "displaybutton":button
    })
    
        
@login_required(login_url="login")
def following(request):
    user = request.user
    profile = Profile.objects.get(user = user)

    #Creating an empty queryset
    posts = Posts.objects.none()
    #To merge the various queryset
    for person in profile.following.all():
        posts = posts | Posts.objects.filter(posterUsername = person)

    posts = posts.order_by("-dateTime").all()
    #paginating the posts
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    
    return render(request, "network/index.html",{
        "posts": page_obj
    })

@login_required(login_url="login")
def followUnfollow(request, profileId):
    #To get the profile of someone
    profile = Profile.objects.get(id = profileId)
    #Getting the current user profile
    profile2 = Profile.objects.get(user = request.user)
    followers = profile.follower.count()

    try:
        #To unfollow
        profile.follower.get(username=request.user)
        profile.follower.remove(request.user)
        profile2.following.remove(profile.user)
        followers -= 1
        button = "Follow" 
    except:
        #To follow
        profile.follower.add(request.user)
        profile2.following.add(profile.user)
        followers += 1
        button = "unFollow"

    profile.save()
    profile2.save()

    #Data to send back
    responseData = {
        "followers": followers,
        "buttontype": button
    }

    return JsonResponse(responseData, safe=False)

@login_required(login_url="login")
def updatePost(request, postId):
    if request.method == "PUT":
        updated_post = Posts.objects.get(id=postId)
        data = json.loads(request.body)
        updated_content = data.get("content", "")
        updated_post.postContent = updated_content
        updated_post.save()

        return JsonResponse({"message": "Post Updated Successfully."}, status=201)

@login_required(login_url="login")
def likePost(request, postId):
    liked_post = Posts.objects.get(id=postId) 
    likes = liked_post.likers.count()
    #likes = liked_post.like
    
    try:
        liked_post.likers.get(username=request.user)
        liked_post.likers.remove(request.user)
        likes -= 1
        like = True
    except:
        liked_post.likers.add(request.user)
        likes += 1
        like = False

    liked_post.like = likes
    liked_post.save()


    print(liked_post.likers.all())

    responsedata = {
        "likes": likes,
        "like": like
    }
    
    return JsonResponse(responsedata, safe=False)

@login_required(login_url="login")
def createComment(request, postId):
    post = Posts.objects.get(id=postId)
    data = json.loads(request.body)
    content = data.get("content", "")

    new_comment = Comment(
        comment = content,
        commentor = request.user,
        comment_item = post
    )
    new_comment.save()
    return JsonResponse({"message": "Comment Created Successfully."}, status=201)

def displayComments(request, postId):
    post = Posts.objects.get(id=postId)

    comments = Comment.objects.filter(comment_item=post).order_by('-id')
    return render(request,"network/Comments.html",{
        "comments": comments
    })