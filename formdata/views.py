from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def show_form(request):
    """Show the form to the user."""

    template_name = "formdata/form.html"
    return render(request, template_name)


def submit(request):
    """Process the form submission and generate a result."""

    template_name = "formdata/confirmation.html"
    print(request.POST)

    # Check if POST data was sent with the HTTP POST messages
    if request.POST:

        # Extract form fields into variables
        name = request.POST["name"]
        favorite_color = request.POST["favorite_color"]

        # Create context variables for use in the template
        context = {
            "name": name,
            "favorite_color": favorite_color,
        }


    return render(request, template_name, context)