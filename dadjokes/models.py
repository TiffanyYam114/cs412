# File: dadjokes/models.py
# Author: Tiffany Yam (tiffyam@bu.edu), 11/12/26
# Description: Contains data models specific to the dadjokes app.

from django.db import models

# Create your models here.

class Joke(models.Model):
    """Models the data attributes of a Joke."""

    text = models.TextField(blank=True)
    name = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a string representation of this Joke."""
        return f"{self.text}"


class Picture(models.Model):
    """Models the data attributes of a Picture."""

    image_url = models.URLField(blank=True)
    name = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)