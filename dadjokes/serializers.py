# File: dadjokes/serializers.py
# Author: Tiffany Yam (tiffyam@bu.edu), 11/12/26
# Description: Convert the data models to a text-representation 
# suitable to transmit over HTTP.
 
from rest_framework import serializers
from .models import *
 
class JokeSerializer(serializers.ModelSerializer):
    """
    A serializer for the Joke model.
    Specify which model/fields to send in the API.
    """
    
    class Meta:
        model = Joke
        fields = ["text", "name", "timestamp"]
    
    def create(self, validated_data):
        '''Override the superclass method that handles object creation.'''

        print(f'JokeSerializer.create, validated_data={validated_data}.')
        # Create a Joke object
        joke = Joke(**validated_data)
        # Save the Joke to the database
        joke.save()
        # return an object instance
        return joke


class PictureSerializer(serializers.ModelSerializer):
    """
    A serializer for the Picture model.
    Specify which model/fields to send in the API.
    """

    class Meta:
        model = Picture
        fields = ["image_url", "name", "timestamp"]
    
    def create(self, validated_data):
        '''Override the superclass method that handles object creation.'''

        print(f'PictureSerializer.create, validated_data={validated_data}.')
        # Create a Picture object
        picture = Picture(**validated_data)
        # Save the Joke to the database
        picture.save()
        # return an object instance
        return picture