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