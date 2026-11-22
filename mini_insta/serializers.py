# File: mini_insta/serializers.py
# Author: Tiffany Yam (tiffyam@bu.edu), 11/20/26
# Description: Convert the data models for the mini_insta app 
# to a text-representation suitable to transmit over HTTP.

from rest_framework import serializers
from .models import *

class ProfileSerializer(serializers.ModelSerializer):
    """
    A serializer for the Profile model.
    Specify which model/fields to send in the API.
    """
    
    class Meta:
        model = Profile
        fields = ["username", "display_name", "profile_image_url", "bio_text", "join_date", "user"]


class PhotoSerializer(serializers.ModelSerializer):
    """
    A serializer for the Photo model.
    Specify which model/fields to send in the API.
    """

    class Meta:
        model = Photo
        fields = ["post", "image_url", "image_file", "timestamp"]
    

class PostSerializer(serializers.ModelSerializer):
    """
    A serializer for the Post model.
    Specify which model/fields to send in the API.
    """

    photos = PhotoSerializer(source="photo_set", many=True, read_only=True)
    
    class Meta:
        model = Post
        fields = ["profile", "timestamp", "caption", "photos"]
    
    def create(self, validated_data):
        """Override the superclass method that handles object creation."""

        print(f"PostSerializer.create, validated_data={validated_data}.")
        # Create a Post object
        post = Post(**validated_data)
        # Save the Post to the database
        post.save()
        # Return an object instance
        return post