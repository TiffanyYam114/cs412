# File: dadjokes/urls.py
# Author: Tiffany Yam (tiffyam@bu.edu), 11/12/26
# Description: Contains url paths for the dadjokes app.

from django.urls import path
from .views import *

urlpatterns = [
    path(r"", RandomJokeView.as_view(), name="joke"), 
    path(r"random", RandomJokeView.as_view(), name="joke"), 
    path(r"jokes", AllJokesView.as_view(), name="all_jokes"), 
    path(r"joke/<int:pk>", ShowJokeView.as_view(), name="joke"), 
    path(r"pictures", AllPicturesView.as_view(), name="pictures"), 
    path(r"picture/<int:pk>", ShowPictureView.as_view(), name="picture"), 
    # API views:
    path(r"api/", RandomJokeDetailAPIView.as_view()), 
    path(r"api/random", RandomJokeDetailAPIView.as_view()), 
    path(r"api/jokes/", JokeListAPIView.as_view()), 
    path(r"api/joke/<int:pk>", JokeDetailAPIView.as_view()), 
    path(r"api/pictures/", PictureListAPIView.as_view()), 
    path(r"api/picture/<int:pk>", PictureDetailAPIView.as_view()), 
    path(r"api/random_picture", RandomPictureDetailAPIView.as_view())
]