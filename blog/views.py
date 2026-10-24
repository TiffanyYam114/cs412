"""Views for the blog application"""

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Article, Comment
from .forms import CreateArticleForm, CreateCommentForm, UpdateArticleForm
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

import random

# Create your views here.

class ShowAllView(ListView):
    """Define a view class to show all blog Articles."""

    model = Article
    template_name = "blog/show_all.html"
    context_object_name = "articles"

    def dispatch(self, request, *args, **kwargs):
        """Override the dispatch method to add debugging information."""

        if request.user.is_authenticated:
            print(f"ShowAllView.dispatch(): request.user={request.user}")
        else:
            print(f"ShowAllView.dispatch(): not logged in")

        return super().dispatch(request, *args, **kwargs)


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


class CreateArticleView(LoginRequiredMixin, CreateView):
    """A view to handle creation of a new Article.
    (1) Display the HTML form to user (GET)
    (2) Process the form submission and store the new Article object (POST)
    """

    form_class = CreateArticleForm
    template_name = "blog/create_article_form.html"

    def get_login_url(self):
        """Return the URL for this app's login page."""
        return reverse("login")

    def form_valid(self, form):
        """Override the default method to add some debugging information."""

        # Print out the form data
        print(f"CreateArticleView.form_valid(): {form.cleaned_data}")

        # Find the logged in user
        user = self.request.user
        print(f"CreateArticleView.form_valid(): {user}")

        # Attach that user to the form instance (to the Article object)
        form.instance.user = user

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


class UpdateArticleView(UpdateView):
    """View class to handle update of an Article based on its PK."""

    model = Article
    form_class = UpdateArticleForm
    template_name = "blog/update_article_form.html"


class DeleteCommentView(DeleteView):
    """View class to delete a Comment on an Article."""

    model = Comment
    template_name = "blog/delete_comment_form.html"

    def get_success_url(self):
        """Return the URL to redirect to after a successful delete."""

        # Find the PK for this comment:
        pk = self.kwargs["pk"]
        # Find the Comment object:
        comment = Comment.objects.get(pk=pk)

        # Find the PK of the Article to which this comment is associated:
        article = comment.article

        return reverse('article', kwargs={"pk": article.pk})


class UserRegistrationView(CreateView):
    """A view to show/process the registration form to create a new User."""

    model = User
    template_name = "blog/register.html"
    form_class = UserCreationForm

    def get_success_url(self):
        """The URL to redirect to after creating a new User."""
        return reverse('login')