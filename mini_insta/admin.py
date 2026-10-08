# File: mini_insta/admin.py
# Author: Tiffany Yam (tiffyam@bu.edu), 9/29/26
# Description: Registers models with the admin


from django.contrib import admin

# Register your models here.

from .models import Profile, Post, Photo
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Photo)