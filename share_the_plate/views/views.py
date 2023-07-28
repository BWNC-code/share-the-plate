from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.db.models import Q
from django.contrib.auth import login
from .forms import SignUpForm, RecipeForm, CommentForm
from cloudinary import CloudinaryImage


# Create your views here.
def home_page(request):
    """
    Display the home page.

    :param request: HTTP request
    :return: Rendered home page
    """
    return render(request, "share_the_plate/index.html")
