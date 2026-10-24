# File: mini_insta/models.py
# Author: Tiffany Yam (tiffyam@bu.edu), 9/29/26
# Description: Contains models for the mini_insta app


from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    """Models the data of an individual user profile"""

    # Define the data attributes of the Profile object
    username = models.TextField(blank=True)
    display_name = models.TextField(blank=True)
    profile_image_url = models.URLField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """Return a string representation of this Profile"""
        return f"{self.username}"

    def get_all_posts(self):
        """Return a QuerySet of all Posts under this Profile"""
        posts = Post.objects.filter(profile=self)
        posts.order_by("-timestamp")
        return posts

    def get_absolute_url(self):
        """Return a URL for this Profile"""
        return reverse("show_profile", kwargs={"pk": self.pk})

    def get_followers(self):
        """Return a list of Profiles following this Profile"""

        # Get the QuerySet of all Follows for which the profile field is this Profile
        follows = Follow.objects.filter(profile=self)

        # Add all the Profile objects in the QuerySet to a list
        followers = []
        for follow in follows:
            followers.append(follow.follower_profile)

        return followers

    def get_num_followers(self):
        """Returns the number of followers this Profile has"""

        # Get the QuerySet of all Follows for which the profile field is this Profile
        follows = Follow.objects.filter(profile=self)

        # Return the length of the QuerySet, which is how many followers there are
        return len(follows)

    def get_following(self):
        """Returns a list of Profiles followed by this Profile"""

        # Get the QuerySet of all Follows for which the follower_profile field is this Profile
        follows = Follow.objects.filter(follower_profile=self)

        # Add all the Profile objects in the QuerySet to a list
        following = []
        for follow in follows:
            following.append(follow.profile)

        return following

    def get_num_following(self):
        """Returns the number of Profiles being followed by this Profile"""

        # Get the QuerySet of all Follows for which the follower_profile field is this Profile
        follows = Follow.objects.filter(follower_profile=self)

        # Return the length of the QuerySet, which is how many Profiles are being followed by this Profile
        return len(follows)

    def get_post_feed(self):
        """Returns a QuerySet of Posts for a Profile's following"""

        # Get a list of Profiles followed by this Profile
        following = self.get_following()

        # Get the QuerySet of all Posts by these Profiles
        posts = Post.objects.filter(profile__in=following)
        # Order by timestamp descending
        posts = posts.order_by("-timestamp")

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

    def get_absolute_url(self):
        """Return a URL for this Post's detail page."""
        return reverse("show_post", kwargs={"pk": self.pk})

    def get_all_photos(self):
        """Return a QuerySet of all Photos in this Post"""
        photos = Photo.objects.filter(post=self)
        return photos

    def get_all_comments(self):
        """Return a QuerySet of all Comments under this Post"""
        comments = Comment.objects.filter(post=self)
        return comments

    def get_likes(self):
        """Returns a list of Profiles that liked a Post"""

        # Get the QuerySet of all Likes under this post
        likes_queryset = Like.objects.filter(post=self)

        # Add all the Profile objects in the QuerySet to a list
        likes = []
        for like in likes_queryset:
            likes.append(like.profile)

        return likes


class Photo(models.Model):
    """Models the data attributes of an image associated with a Post"""

    # Define the data attributes of the Photo object
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.URLField(blank=True)
    image_file = models.ImageField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a string representation of this Photo"""
        if self.image_url != "":
            return f"{self.image_url}"
        elif self.image_file:
            return f"{self.image_file.url}"

    def get_image_url(self):
        if self.image_url != "":
            return self.image_url
        elif self.image_file:
            return self.image_file.url


class Follow(models.Model):
    """Models the data attributes related to a Profile following another Profile"""

    profile = models.ForeignKey(Profile, related_name="profile", on_delete=models.CASCADE)
    follower_profile = models.ForeignKey(Profile, related_name="follower_profile", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a string representation of this Follow"""
        return f"{self.follower_profile.username} follows {self.profile.username}"


class Comment(models.Model):
    """Models a Profile commenting on another Profile's Post"""

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    text = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a string representation of this Comment"""
        return f"{self.profile} commented: {self.text}"


class Like(models.Model):
    """Models a Profile liking a Post"""

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a string representation of this Like"""
        return f"{self.profile.username} liked {self.post.profile.username}'s post: {self.post}"