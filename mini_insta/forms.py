# File: mini_insta/forms.py
# Author: Tiffany Yam (tiffyam@bu.edu), 10/5/26
# Description: Forms for the mini_insta app


from django import forms
from .models import *

class CreatePostForm(forms.ModelForm):
    """A form to add a Post to the database"""

    class Meta:
        """Relate this form to the Post model"""
        model = Post
        fields = ["caption"]


class UpdateProfileForm(forms.ModelForm):
    """A form to update a Profile"""

    class Meta:
        """Relate this form to the Profile model"""
        model = Profile
        fields = ["display_name", "profile_image_url", "bio_text"]