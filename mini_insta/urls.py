# File: mini_insta/urls.py
# Author: Tiffany Yam (tiffyam@bu.edu), 9/29/26
# Description: Contains URLs specific to the mini_insta app


from django.urls import path
from .views import ProfileListView, ProfileDetailView

urlpatterns = [
    path('', ProfileListView.as_view(), name="show_all_profiles"),
    path('show_all/', ProfileListView.as_view(), name="show_all_profiles"),
    path('profile/<int:pk>', ProfileDetailView.as_view(), name="show_profile"),
]