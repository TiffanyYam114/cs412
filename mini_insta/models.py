# File: mini_insta/models.py
# Author: Tiffany Yam (tiffyam@bu.edu), 9/29/26
# Description: Contains models for the mini_insta app


from django.db import models

# Create your models here.

class Profile(models.Model):
    """Models the data of an individual user profile"""

    # Define the data attributes of the Profile object
    username = models.TextField(blank=True)
    display_name = models.TextField(blank=True)
    profile_image_url = models.URLField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateField(auto_now=True)

    def __str__(self):
        """Return a string representation of this Profile"""
        return f"{self.username}"

    def get_all_posts(self):
        """Return a QuerySet of all Posts under this Profile"""
        posts = Post.objects.filter(profile=self)
        posts.order_by("-timestamp")
        return posts


class Post(models.Model):
    """Models the data attributes of an Instagram post"""

    # Define the data attributes of the Post object
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    caption = models.TextField(blank=True)

    def __str__(self):
        """Return a string representation of this Post"""
        return f"{self.caption}"

    def get_all_photos(self):
        """Return a QuerySet of all Photos in this Post"""
        photos = Photo.objects.filter(post=self)
        return photos


class Photo(models.Model):
    """Models the data attributes of an image associated with a Post"""

    # Define the data attributes of the Photo object
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.URLField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a string representation of this Photo"""
        return f"{self.image_url}"