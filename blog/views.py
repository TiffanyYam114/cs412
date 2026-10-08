"""Views for the blog application"""

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Article
from .forms import CreateArticleForm, CreateCommentForm
from django.urls import reverse

import random

# Create your views here.

class ShowAllView(ListView):
    """Define a view class to show all blog Articles."""

    model = Article
    template_name = "blog/show_all.html"
    context_object_name = "articles"


class ArticleView(DetailView):
    """Display a single article."""

    model = Article
    template_name = "blog/article.html"
    context_object_name = "article"


class RandomArticleView(DetailView):
    """Display a single article selected at random."""

    model = Article
    template_name = "blog/article.html"
    context_object_name = "article"

    # Methods
    def get_object(self):
        """Return one instance of the Article object selected at random."""

        all_articles = Article.objects.all()
        article = random.choice(all_articles)
        return article


class CreateArticleView(CreateView):
    """A view to handle creation of a new Article.
    (1) Display the HTML form to user (GET)
    (2) Process the form submission and store the new Article object (POST)
    """

    form_class = CreateArticleForm
    template_name = "blog/create_article_form.html"

    def form_valid(self, form):
        """Override the default method to add some debugging information."""

        # Print out the form data
        print(f"CreateArticleView.form_valid(): {form.cleaned_data}")

        # Delegate work to the superclass to do the rest
        return super().form_valid(form)


class CreateCommentView(CreateView):
    """A view to handle creation of a new Comment on an Article."""

    form_class = CreateCommentForm
    template_name = "blog/create_comment_form.html"

    def get_success_url(self):
        """Provide a URL to redirect to after creating a new Comment."""

        # Create and return a URL
        # return reverse("show_all")
        # Retrieve the PK from the URL pattern
        pk = self.kwargs["pk"]
        # Call reverse to generate the URL for this Article
        return reverse("article", kwargs={"pk": pk})

    def get_context_data(self):
        """Return the dictionary of context variables for use in the template."""

        # Calling the superclass method
        context = super().get_context_data()

        # Find/add the article to the context data
        pk = self.kwargs["pk"]
        article = Article.objects.get(pk=pk)

        # Add this article into the context dictionary
        context["article"] = article

        return context

    def form_valid(self, form):
        """This method handles the form submission and saves the new 
        object to the Django database. 
        We need to add the foreign key (of the new Article) to the 
        Comment object before saving it to the database.
        """

        print(form.cleaned_data)
        # Retrieve the PK from the URL pattern
        pk = self.kwargs["pk"]
        article = Article.objects.get(pk=pk)
        # Attach this Article to the Comment
        form.instance.article = article # Set the PK

        # Delegate the work to the superclass method form_valid
        return super().form_valid(form)