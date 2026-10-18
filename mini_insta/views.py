# File: mini_insta/views.py
# Author: Tiffany Yam (tiffyam@bu.edu), 9/29/26
# Description: Contains views for the mini_insta app


from typing import Any

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Profile, Post, Photo
from .forms import CreatePostForm, UpdateProfileForm, UpdatePostForm
from django.urls import reverse

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


class UpdateProfileView(UpdateView):
    """Display the form to update a Profile"""

    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_insta/update_profile_form.html"


class DeletePostView(DeleteView):
    """Delete a Post"""

    model = Post
    template_name = "mini_insta/delete_post_form.html"

    def get_context_data(self, **kwargs):
        """Return the context dictionary for use in the template"""

        # Get the context dictionary from the superclass
        context = super().get_context_data(**kwargs)

        # Find the PK of this Post
        pk = self.kwargs["pk"]
        # Find the Post object
        post = Post.objects.get(pk=pk)

        # Find the Profile associated with this Post
        profile = post.profile

        # Add the Post and Profile to the context dictionary
        context["post"] = post
        context["profile"] = profile

        return context

    def get_success_url(self):
        """Redirect to the Profile page after a successful delete"""

        # Find the PK of this Post
        pk = self.kwargs["pk"]
        # Find the Post object
        post = Post.objects.get(pk=pk)

        # Find the Profile associated with this post
        profile = post.profile
        
        return reverse("show_profile", kwargs={"pk": profile.pk})


class UpdatePostView(UpdateView):
    """Display the form to update a Post"""

    model = Post
    form_class = UpdatePostForm
    template_name = "mini_insta/update_post_form.html"


class ShowFollowersView(DetailView):
    """A view to show the followers of a Profile"""

    model = Profile
    template_name = "mini_insta/show_followers.html"
    context_object_name = "profile"


class ShowFollowingView(DetailView):
    """A view to show the Profiles a Profile is following"""

    model = Profile
    template_name = "mini_insta/show_following.html"
    context_object_name = "profile"


class ShowFeedView(DetailView):
    """A view to show the feed for a Profile"""

    model = Post
    template_name = "mini_insta/show_feed.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        """Return the context dictionary for use in the template"""

        # Get the context dictionary from the superclass
        context = super().get_context_data()

        # Find the Profile associated with this Post
        pk = self.kwargs["pk"]
        profile = Profile.objects.get(pk=pk)

        # Add the Profile to the context dictionary
        context["profile"] = profile

        return context


class SearchView(ListView):
    """A view to search for Profiles and Posts"""

    model = Profile
    template_name = "mini_insta/search_results.html"

    def dispatch(self, request, *args, **kwargs):
        if request.GET.get("query"):
            return super().dispatch(request, *args, **kwargs)
        else:
            pk = self.kwargs["pk"]
            profile = Profile.objects.get(pk=pk)
            context = {
                "profile": profile
            }
            return render(request, "mini_insta/search.html", context)

    def get_queryset(self):
        """Return the QuerySet of Posts that contain the query"""

        # Get the query
        query = self.request.GET.get("query")

        # Get all Posts whose caption contains the query
        posts = Post.objects.filter(caption__contains=query)

        return posts

    def get_queryset_profiles(self):
        """Return the QuerySet of Profiles that contain the query"""

        # Get the query
        query = self.request.GET.get("query")

        # Get all Profiles whose username, display name, or bio text contain the query
        profiles = []
        for profile in Profile.objects.all():
            if query in profile.username or query in profile.display_name or query in profile.bio_text:
                profiles.append(profile)

        return profiles

    def get_context_data(self, **kwargs):
        """Returns the dictionary of context data to be used in the template"""

        # Get the context dictionary from the superclass
        context = super().get_context_data()

        # Find the Profile
        pk = self.kwargs["pk"]
        profile = Profile.objects.get(pk=pk)
        context["profile"] = profile

        # Find the query if it exists
        if self.request.GET.get("query"):
            context["query"] = self.request.GET.get("query")

        # Get the Posts that match the query
        posts = self.get_queryset()
        context["posts"] = posts

        # Get the Profiles that match the query
        profiles = self.get_queryset_profiles()
        context["profiles"] = profiles

        return context