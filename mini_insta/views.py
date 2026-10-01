# File: mini_insta/views.py
# Author: Tiffany Yam (tiffyam@bu.edu), 9/29/26
# Description: Contains views for the mini_insta app


from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Profile

# Create your views here.

class ProfileListView(ListView):
    """Display all Profiles"""

    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    context_object_name = "profiles"

class ProfileDetailView(DetailView):
    """Display one Profile"""

    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"