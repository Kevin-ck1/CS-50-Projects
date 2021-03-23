from django.contrib import admin

from .models import User, Posts, Comment, Like, Follower

# Register your models here.

admin.site.register(User)
admin.site.register(Posts)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Follower)