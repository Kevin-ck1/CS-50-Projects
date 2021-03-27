
from django.urls import path

from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newPost", views.new, name="new"),
    path("allPost", views.allPost, name="allPost"),
    path("profile/<str:profilename>", views.profile, name="profile"),
    path("following", views.following, name="following"),
    path("followUnfollow/<str:profileId>", views.followUnfollow, name="followUnfollow"),
    path("updatePost/<int:postId>", views.updatePost, name="updatePost"),
    path("likePost/<int:postId>", views.likePost, name="likePost")
]  

