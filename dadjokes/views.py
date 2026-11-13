# File: dadjokes/views.py
# Author: Tiffany Yam (tiffyam@bu.edu), 11/12/26
# Description: Contains views for the dadjokes app.

from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from .models import Joke, Picture

# REST API:
from rest_framework import generics
from .serializers import *

import random

# Create your views here.

class RandomJokeView(TemplateView):
    """Display one Joke and one Picture selected at random."""

    template_name = "dadjokes/joke.html"
    
    def get_context_data(self):
        """Return the context dictionary for use in the template."""

        context = super().get_context_data()

        # Get all Jokes and Pictures
        all_jokes = Joke.objects.all()
        all_pictures = Picture.objects.all()

        # Select a Joke and Picture at random
        joke = random.choice(all_jokes)
        picture = random.choice(all_pictures)

        context["joke"] = joke
        context["picture"] = picture

        return context


class ShowJokeView(DetailView):
    """Display one Joke."""

    model = Joke
    template_name = "dadjokes/joke.html"
    context_object_name = "joke"


class AllJokesView(ListView):
    """Display all Jokes."""

    model = Joke
    template_name = "dadjokes/all_jokes.html"
    context_object_name = "jokes"


class AllPicturesView(ListView):
    """Display all Pictures."""

    model = Picture
    template_name = "dadjokes/all_pictures.html"
    context_object_name = "pictures"


class ShowPictureView(DetailView):
    """Display one Picture."""

    model = Picture
    template_name = "dadjokes/picture.html"
    context_object_name = "picture"


class JokeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """API View to display one Joke."""

    queryset = Joke.objects.all()
    serializer_class = JokeSerializer


class RandomJokeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """API View to display one Joke selected at random."""

    serializer_class = JokeSerializer

    def get_object(self):
        """Return one Joke object selected at random."""

        all_jokes = Joke.objects.all()
        joke = random.choice(all_jokes)
        return joke


class JokeListAPIView(generics.ListCreateAPIView):
    """API view to display all Jokes and to create an Joke."""

    queryset = Joke.objects.all()
    serializer_class = JokeSerializer


class PictureDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """API View to display one Picture."""

    queryset = Picture.objects.all()
    serializer_class = PictureSerializer


class RandomPictureDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """API View to display one Picture selected at random."""
    
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer

    def get_object(self):
        """Return one Picture object selected at random."""

        all_pictures = Picture.objects.all()
        picture = random.choice(all_pictures)
        return picture


class PictureListAPIView(generics.ListCreateAPIView):
    """API view to display all Pictures and to create an Picture."""
    
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer