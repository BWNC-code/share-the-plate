from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from .models import *
from django.contrib.auth import login
from .forms import SignUpForm


# Create your views here.
def home_page(request):
    return render(request, 'share_the_plate/index.html')


def recipe_list(request):
    # Get the 10 most recent recipes
    recipes = Recipe.objects.order_by('-created_at')[:10]

    context = {
        'recipes': recipes
    }

    return render(request, 'share_the_plate/recipe_list.html', context)


def recipe_detail(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    return render(request,
                  'share_the_plate/recipe_detail.html', {'recipe': recipe})


class CustomLoginView(LoginView):
    template_name = 'share_the_plate/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        if self.request.user is not None:
            return reverse_lazy('share_the_plate:profile_info', kwargs={'username': self.request.user.username})
        return super().get_success_url()


def after_logout(request):
    return render(request, 'share_the_plate/after_logout.html')


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('share_the_plate:recipe_list')
        else:
            print(form.errors)  # print form errors if form is not valid
    else:
        form = SignUpForm()
    return render(request, 'share_the_plate/sign_up.html', {'form': form})


@login_required
def profile_info(request, username):
    if request.user.username != username:
        return redirect('share_the_plate:index')
    user = User.objects.get(username=username)
    return render(request, 'share_the_plate/profile_info.html', {'profile_user': user})


@login_required
def user_recipes(request, username):
    if request.user.username != username:
        return redirect('share_the_plate:index')
    user = User.objects.get(username=username)
    recipes = Recipe.objects.filter(user=user)
    return render(request, 'share_the_plate/user_recipes.html', {'profile_user': user, 'recipes': recipes})


@login_required
def liked_recipes(request, username):
    if request.user.username != username:
        return redirect('share_the_plate:index')
    user = User.objects.get(username=username)
    likes = Like.objects.filter(user=user)
    return render(request, 'share_the_plate/liked_recipes.html', {'profile_user': user, 'likes': likes})