from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Posts(models.Model):
    posterUsername = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_creator")
    postContent = models.CharField(max_length=64)
    dateTime =  models.DateTimeField(auto_now_add=True)
    likers = models.ManyToManyField(User, related_name="post_likers")
    like = models.IntegerField()

    # def __str__(self):
    #     return self.id 
    def serialize(self):
        return {
            "id": self.id,
            "poster": self.posterUsername.username,
            "content": self.postContent,
            "dateTime": self.dateTime.strftime("%b %d %Y, %I:%M %p"),
            "like": self.like
        }


class Comment(models.Model):
    comment = models.CharField(max_length=64)
    commentor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_commentor")
    comment_item = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name="post_comment")

class Like(models.Model):
    liked_post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name="liked")
    liker = models.ManyToManyField(User, related_name="post_liker")
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    usermail = models.CharField(max_length=64)
    follower =  models.ManyToManyField(User, blank=True, related_name="my_followers")
    following =  models.ManyToManyField(User, blank=True, related_name="my_following")
