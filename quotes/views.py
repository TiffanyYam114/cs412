# File: views.py
# Author: Tiffany Yam (tiffyam@bu.edu), 9/15/26
# Description: Contains the quotes and images lists, and sends necessary 
# context variables to their respective html files. 



from django.shortcuts import render

import random

# Create your views here.

# Contains all quotes
quotes = [
    "I like being like a chameleon who transforms himself with each role.", 

    "I get attached to things: I wear the same jeans for a year.", 

    "A movie set is like a petri dish for neuroses, you know? It's just, like, "
    "egos and weird personalities and, more than anything, fear.", 
]

# Contains all images
images = [
    "https://static.wikia.nocookie.net/xmenmovies/images/8/89/Oscar_Isaac.jpg/revision/latest?cb=20180523155622", 
    "https://hips.hearstapps.com/hmg-prod/images/b960767c-6f1d-4772-8035-6b5156dae9e0.jpeg?crop=0.952xw:1xh;0.024xw,0xh", 
    "https://thumb.wikimedia.org/wikipedia/commons/thumb/0/0d/Oscar_Isaac_at_82nd_Venice_International_Film_Festival-1_%28cropped%29.jpg/960px-Oscar_Isaac_at_82nd_Venice_International_Film_Festival-1_%28cropped%29.jpg?utm_source=en.wikipedia.org&utm_campaign=index&utm_content=thumbnail", 
]


def quote(request):
    """Respond to the URL 'quote', delegate work to quote.html"""

    template_name = 'quote.html'

    # Pick a random quote and image and send them in context variable
    context = {
        "random_quote": quotes[random.randint(0, 2)],
        "random_image": images[random.randint(0, 2)],
    }

    return render(request, template_name, context)


def show_all(request):
    """Respond to the URL 'show_all', delegate work to show_all.html"""

    template_name = 'show_all.html'

    # Send all 3 quotes and images in their own context variables
    context = {
        "quote1": quotes[0],
        "quote2": quotes[1],
        "quote3": quotes[2],
        "image1": images[0],
        "image2": images[1],
        "image3": images[2],
    }

    return render(request, template_name, context)


def about(request):
    """Respond to the URL 'about', delegate work to about.html"""

    template_name = 'about.html'
    return render(request, template_name)