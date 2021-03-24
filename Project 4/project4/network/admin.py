from django.contrib import admin

from .models import User, Posts, Comment, Like, Profile

# Register your models here.

admin.site.register(User)
admin.site.register(Posts)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Profile)