# File: restaurant/urls.py
# Author: Tiffany Yam (tiffyam@bu.edu), 9/22/26
# Description: Contains URLs specific to the restaurant app



from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    path(r'', views.main, name="main"),
    path(r'order', views.order, name="order"),
    path(r'confirmation', views.confirmation, name="confirmation"),
]