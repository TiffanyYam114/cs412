# File: voter_analytics/urls.py
# Author: Tiffany Yam (tiffyam@bu.edu), 10/29/26
# Description: Contains urls specific to the voter_analytics app.

from django.urls import path
from . import views

urlpatterns = [
    path(r"", views.VoterListView.as_view(), name="voters"), 
    path(r"voters", views.VoterListView.as_view(), name="voters_list"), 
    path(r"voter/<int:pk>", views.VoterDetailView.as_view(), name="voter"), 
    path(r"graphs", views.GraphsListView.as_view(), name="graphs"), 
]