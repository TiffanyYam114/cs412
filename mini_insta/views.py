# File: mini_insta/views.py
# Author: Tiffany Yam (tiffyam@bu.edu), 9/29/26
# Description: Contains views for the mini_insta app


from typing import Any

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Profile, Post, Photo
from .forms import CreatePostForm

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

    
    

class PostDetailView(DetailView):
    """Display one Post"""

    model = Post
    template_name = "mini_insta/show_post.html"
    context_object_name = "post"


class CreatePostView(CreateView):
    """Create a new Post"""

    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"

    def get_context_data(self):
        """Return the context dictionary for use in the template"""

        # Get the context dictionary from the superclass
        context = super().get_context_data()

        # Find the Profile associated with this Post
        pk = self.kwargs["pk"]
        profile = Profile.objects.get(pk=pk)

        # Add the Profile to the context dictionary
        context["profile"] = profile

        return context

    def form_valid(self, form):
        """Attach a Profile object to this Post"""

        # Find/add the Profile to the context data
        pk = self.kwargs["pk"]
        profile = Profile.objects.get(pk=pk)
        
        # Attach the Profile to the Post
        form.instance.profile = profile

        # Save the Post before attaching Photos to it.
        response = super().form_valid(form)

        # if self.request.POST:
        #     image_url = self.request.POST.get("image_url")
        #     Photo.objects.create(post=self.object, image_url=image_url)

        files = self.request.FILES.getlist('files')

        # Create a new Photo for every uploaded image
        for file in files:
            Photo.objects.create(post=self.object, image_file=file)
        
        return response
