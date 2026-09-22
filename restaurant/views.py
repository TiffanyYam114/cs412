# File: restaurant/views.py
# Author: Tiffany Yam (tiffyam@bu.edu), 9/22/26
# Description: Contains list daily_specials and dict menu. Displays HTML pages 
# when their link is clicked.



from django.shortcuts import render

import random
import time

# Create your views here.


# List of all daily specials
daily_specials = [
    ["Scallion Pancake", 7.00],
    ["Popcorn Chicken", 8.50],
    ["Pork Gyoza", 8.00],
    ["Takoyaki", 8.50],
    ["Fried Spicy Boneless Chicken", 9.00]
]

# Dictionary of all menu items
menu = {
    "pork_chop_ns": ["Pork Chop Noodle Soup", 14.50],
    "sliced_beef_ns": ["Sliced Beef Noodle Soup", 14.50],
    "fish_fillet_ns": ["Fish Fillet Noodle Soup", 14.50],
    "beef_tripe_ns": ["Beef Tripe Noodle Soup", 15.00],
    "soy_egg": ["Soy Egg", 2.00],
    "beef_slices": ["Beef Slices", 4.00],
    "fish_tofu": ["Fish Tofu", 3.00],
    "napa_cabbage": ["Napa Cabbage", 2.50],
    "noodles": ["Noodles", 2.00]
}


def main(request):
    """Respond to the URL 'main', delegate work to main.html"""

    template_name = "restaurant/main.html"
    return render(request, template_name)


def order(request):
    """Respond to the URL 'order', delegate work to order.html"""

    template_name = "restaurant/order.html"

    # Pick a random daily special and send it in the context variable
    context = {
        "daily_special": daily_specials[random.randint(0, 4)],
    }

    return render(request, template_name, context)


def confirmation(request):
    """Respond to the URL 'confirmation', delegate work to confirmation.html"""

    template_name = "restaurant/confirmation.html"
    print(request.POST)

    if request.POST:

        ordered_items = []
        total = 0

        # Check if each menu item is in the POST. If it is, add it to 
        # ordered_items and increase the total
        for key, value in menu.items():
            if request.POST.get(key):
                ordered_items.append(value)
                total += value[1]

        # print(ordered_items)

        # Check if the customer ordered the daily special, add it to 
        # ordered_items, and increase the total
        if request.POST.get("special"):
            for special in daily_specials:
                if special[0] == request.POST.get("special"):
                    ordered_items.append(special)
                    total += special[1]
                    # There can only be one special, so exit the loop
                    break
            

        # Choose a random pickup time within 30 to 60 minutes of the current time
        minutes_until_ready = random.randint(30, 60)
        # Add random time to current time
        ready_timestamp = time.time() + (minutes_until_ready * 60)
        # Convert timestamp to readable string
        ready_time = time.strftime(
            "%A, %B %d at %I:%M %p", time.localtime(ready_timestamp)
        )


        # Extract customer information
        name = request.POST["name"]
        email = request.POST["email"]
        phone_number = request.POST["phone_number"]

        
        # Create context variable to send customer information and order 
        # information to the template
        context = {
            "name": name,
            "email": email,
            "phone_number": phone_number,
            "ordered_items": ordered_items,
            # Show total with 2 decimal places
            "total": f"{total:.2f}",
            "ready_time": ready_time,
        }

    return render(request, template_name, context)