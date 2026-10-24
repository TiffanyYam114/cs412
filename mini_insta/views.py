# File: mini_insta/views.py
# Author: Tiffany Yam (tiffyam@bu.edu), 9/29/26
# Description: Contains views for the mini_insta app


from typing import Any

from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import *
from .forms import *
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login

# Create your views here.


class CurrentProfile():
    """Get the current logged in user's profile"""

    def get_profile(self, request):
        """Return the current User's Profile"""

        if request.user.is_authenticated:
            user = request.user
            current_profile = Profile.objects.filter(user=user).first()
            print(f"The current profile is: {current_profile}")
            return current_profile
        else:
            return None

    def get_context_data(self, **kwargs):
            """Return the context dictionary for use in the template"""
    
            # Get the context dictionary from the superclass
            context = super().get_context_data(**kwargs)
            current_profile = self.get_profile(self.request)
            context["current_profile"] = current_profile
            return context


class CustomLoginRequiredMixin(LoginRequiredMixin, CurrentProfile):
    """Override the default LoginRequiredMixin class with additional features"""

    def get_login_url(self):
        """Return the URL for the login page"""
        return reverse("login")


class ProfileListView(CurrentProfile, ListView):
    """Display all Profiles"""

    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    context_object_name = "profiles"


class ProfileDetailView(CurrentProfile, DetailView):
    """Display one Profile"""

    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"


class UserProfileDetailView(CurrentProfile, DetailView):
    """Display the current user's Profile"""

    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"

    def get_object(self):
            """Get the object (profile)"""
            return self.get_profile(self.request)

    
class PostDetailView(CurrentProfile, DetailView):
    """Display one Post"""

    model = Post
    template_name = "mini_insta/show_post.html"
    context_object_name = "post"


class CreatePostView(CustomLoginRequiredMixin, CreateView):
    """Create a new Post"""

    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"

    def get_context_data(self, **kwargs):
        """Return the context dictionary for use in the template"""

        # Get the context dictionary from the superclass
        context = super().get_context_data(**kwargs)

        # Find the Profile associated with this Post
        profile = self.get_profile(self.request)

        # Add the Profile to the context dictionary
        context["profile"] = profile

        return context

    def form_valid(self, form):
        """Attach a Profile object to this Post"""

        # Find/add the Profile to the context data
        profile = self.get_profile(self.request)
        
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


class UpdateProfileView(CustomLoginRequiredMixin, UpdateView):
    """Display the form to update a Profile"""

    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_insta/update_profile_form.html"

    def get_object(self):
        """Get the object (profile)"""
        return self.get_profile(self.request)


class DeletePostView(CustomLoginRequiredMixin, DeleteView):
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


class UpdatePostView(CustomLoginRequiredMixin, UpdateView):
    """Display the form to update a Post"""

    model = Post
    form_class = UpdatePostForm
    template_name = "mini_insta/update_post_form.html"


class ShowFollowersView(CurrentProfile, DetailView):
    """A view to show the followers of a Profile"""

    model = Profile
    template_name = "mini_insta/show_followers.html"
    context_object_name = "profile"


class ShowFollowingView(CurrentProfile, DetailView):
    """A view to show the Profiles a Profile is following"""

    model = Profile
    template_name = "mini_insta/show_following.html"
    context_object_name = "profile"


class ShowFeedView(CustomLoginRequiredMixin, DetailView):
    """A view to show the feed for a Profile"""

    model = Post
    template_name = "mini_insta/show_feed.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        """Return the context dictionary for use in the template"""

        # Get the context dictionary from the superclass
        context = super().get_context_data(**kwargs)

        # Find the Profile associated with this Post
        profile = self.get_profile(self.request)

        # Add the Profile to the context dictionary
        context["profile"] = profile

        return context

    def get_object(self):
            """Get the object (profile)"""
            return self.get_profile(self.request)


class SearchView(CustomLoginRequiredMixin, ListView):
    """A view to search for Profiles and Posts"""

    model = Profile
    template_name = "mini_insta/search_results.html"

    def get(self, request, *args, **kwargs):
        if request.GET.get("query"):
            return super().get(request, *args, **kwargs)
        else:
            profile = self.get_profile(self.request)
            context = {
                "profile": profile,
                "current_profile": profile
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
        context = super().get_context_data(**kwargs)

        # Find the Profile
        profile = self.get_profile(self.request)
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


class CreateProfileView(CreateView):
    """Display the form to create a Profile"""

    model = Profile
    form_class = CreateProfileForm
    template_name = "mini_insta/create_profile_form.html"

    def get_context_data(self, **kwargs):
        """Return the context dictionary for use in the template"""

        context = super().get_context_data(**kwargs)

        # Create a UserCreationForm and add it to the context dictionary
        user_creation_form = UserCreationForm()
        context["user_creation_form"] = user_creation_form

        return context

    def form_valid(self, form):
        """Associate the Profile with the User"""

        # Save the form submission as a new User
        user_creation_form = UserCreationForm(self.request.POST)
        user = user_creation_form.save()

        # Log the User in
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')

        # Attach the Profile to the User
        form.instance.user = user

        response = super().form_valid(form)
        return response


class FollowProfileView(CustomLoginRequiredMixin, TemplateView):
    """Follow another Profile"""

    def post(self, request, *args, **kwargs):
        # Get the logged in Profile and the Profile to be followed
        current_profile = self.get_profile(request)
        profile = Profile.objects.get(pk=self.kwargs["pk"])

        # Only allow a follow if the two Profiles are different
        if current_profile != profile:
            Follow.objects.create(profile=profile, follower_profile=current_profile)

        return redirect("show_profile", pk=profile.pk)


class DeleteFollowView(CustomLoginRequiredMixin, TemplateView):
    """Delete a Follow on another Profile"""

    def post(self, request, *args, **kwargs):
        # Get the logged in Profile and the Profile to be unfollowed
        current_profile = self.get_profile(request)
        profile = Profile.objects.get(pk=self.kwargs["pk"])

        # Delete the Follow object
        Follow.objects.get(profile=profile, follower_profile=current_profile).delete()

        return redirect("show_profile", pk=profile.pk)


class LikePostView(CustomLoginRequiredMixin, TemplateView):
    """Like another Profile's Post"""

    def post(self, request, *args, **kwargs):
        # Get the logged in Profile and the Post to be liked
        current_profile = self.get_profile(request)
        post = Post.objects.get(pk=self.kwargs["pk"])

        # Only allow a like if the Post is not associated with the Profile
        if current_profile != post.profile:
            Like.objects.create(post=post, profile=current_profile)

        return redirect("show_post", pk=post.pk)


class DeleteLikeView(CustomLoginRequiredMixin, TemplateView):
    """Delete a Like on a Post"""

    def post(self, request, *args, **kwargs):
        # Get the logged in Profile and the Post to be unliked
        current_profile = self.get_profile(request)
        post = Post.objects.get(pk=self.kwargs["pk"])

        # Delete the Like object
        Like.objects.get(post=post, profile=current_profile).delete()

        return redirect("show_post", pk=post.pk)