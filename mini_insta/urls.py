# File: mini_insta/urls.py
# Author: Tiffany Yam (tiffyam@bu.edu), 9/29/26
# Description: Contains URLs specific to the mini_insta app


from django.urls import path
from .views import Profile

urlpatterns = [
    path('', ShowAllView.as_view(), name="show_all"),
]