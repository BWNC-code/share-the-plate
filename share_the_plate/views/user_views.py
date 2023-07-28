from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import Http404
from .forms import SignUpForm
from django.contrib.auth import login, logout
from ..models import Recipe, Like
from .other_views import check_user_exists
from cloudinary import CloudinaryImage


class CustomLoginView(LoginView):
    """
    Custom login view.

    Inherits from LoginView provided by Django.
    """

    template_name = "share_the_plate/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        """
        Sends user to profile once logged in.
        """
        if self.request.user is not None:
            return reverse_lazy(
                "share_the_plate:profile_info",
                kwargs={"username": self.request.user.username},
            )
        return super().get_success_url()


@login_required
@check_user_exists
def profile_info(request, username):
    """
    Display profile information of the user.

    :param request: HTTP request
    :param username: username of the user
    :return: Rendered profile information page
    """
    if request.user.username != username:
        return redirect("share_the_plate:index")
    user = User.objects.get(username=username)
    return render(request, "share_the_plate/profile_info.html",
                  {"profile_user": user})


@login_required
@check_user_exists
def user_recipes(request, username):
    """
    Display submitted recipes of the user.

    :param request: HTTP request
    :param username: username of the user
    :return: Rendered list of users recipes page
    """
    if request.user.username != username:
        return redirect("share_the_plate:index")
    user = User.objects.get(username=username)
    user_recipes = Recipe.objects.filter(user=user)
    for recipe in user_recipes:
        recipe.featured_image_url = CloudinaryImage(
            str(recipe.featured_image)
        ).build_url(crop="scale")
    return render(
        request,
        "share_the_plate/user_recipes.html",
        {"profile_user": user, "user_recipes": user_recipes},
    )


@login_required
@check_user_exists
def liked_recipes(request, username):
    """
    Display users liked recipes.

    :param request: HTTP request
    :param username: username of the user
    :return: Rendered list of users liked reciped page
    """
    if request.user.username != username:
        return redirect("share_the_plate:index")
    user = User.objects.get(username=username)
    liked_recipes = Recipe.objects.filter(like__user=user)

    return render(
        request,
        "share_the_plate/liked_recipes.html",
        {"profile_user": user, "liked_recipes": liked_recipes},
    )


def after_logout(request):
    return render(request, "share_the_plate/after_logout.html")


def signup(request):
    """
    Handle user registration.
    Display sign up form.

    :param request: HTTP request
    :return: Rendered registration page
    """
    if request.method == "POST":
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user,
                  backend="django.contrib.auth.backends.ModelBackend")
            return redirect("share_the_plate:recipe_list")
        else:
            print(form.errors)  # print form errors if form is not valid
    else:
        form = SignUpForm()
    return render(request, "share_the_plate/sign_up.html", {"form": form})


@login_required
@check_user_exists
def deactivate_confirm(request, username):
    if request.method == 'POST':
        # Ensure the user is deactivating their own account
        User = get_user_model()
        user = get_object_or_404(User, username=username)

        # The user confirmed they want to deactivate their own account.
        # Deactivate it and log them out.
        user.is_active = False
        user.save()
        logout(request)
        return render(request, 'share_the_plate/deactivated_user.html')

    # If the method is not POST, it's GET. So, render the confirmation page
    return render(request, 'share_the_plate/deactivate_confirm.html')


def deactivated_account(request, username):
    # Render the page that informs the user their account has been deactivated.
    return render(request, 'share_the_plate/deactivated_user.html')
