from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from .models import *
from django.contrib.auth import login
from .forms import SignUpForm, RecipeForm
from cloudinary import CloudinaryImage


# Create your views here.
def home_page(request):
    """
    Display the home page.

    :param request: HTTP request
    :return: Rendered home page
    """
    return render(request, 'share_the_plate/index.html')


def recipe_list(request):
    """
    List the 10 most recent recipes.

    :param request: HTTP request
    :return: Rendered list of recipes
    """
    recipes = Recipe.objects.order_by('-created_at')[:10]

    context = {
        'recipes': recipes
    }

    return render(request, 'share_the_plate/recipe_list.html', context)


def recipe_detail(request, slug):
    """
    Display the detail of a specific recipe.

    :param request: HTTP request
    :param slug: Slug of the recipe
    :return: Rendered detail view of the recipe
    """
    recipe = get_object_or_404(Recipe, slug=slug)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.recipe = recipe
            comment.user = request.user
            comment.save()
            return redirect('share_the_plate:recipe_detail', slug=recipe.slug)
    else:
        form = CommentForm()

    return render(request,
                  'share_the_plate/recipe_detail.html',
                  {'recipe': recipe, 'form': form})


class RecipeCreateView(LoginRequiredMixin, CreateView):
    """
    Display a form dor creating a new recipe.
    Only accessed by authenticated user so can set author.

    Inherits LoginRequiredMixin to check user is logged in.
    Inherits from CreateView for the creation process.
    """
    model = Recipe
    form_class = RecipeForm
    template_name = 'share_the_plate/recipe_form.html'

    def form_valid(self, form):
        """
        Set the current user as the author of the recipe before saving.

        :param form: Recipe creation form
        :return: HTTP response
        """
        form.instance.user = self.request.user
        response = super().form_valid(form)
        form.instance.tags.add(*self.request.POST.get('tags').split(","))
        return response


class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'share_the_plate/recipe_form.html'

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user

    def get_login_url(self):
        if not self.request.user.is_authenticated:
            return super().get_login_url()
        else:
            return reverse('share_the_plate:recipe_detail',
                           kwargs={'slug': self.get_object().slug})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if self.request.method == 'POST':
            form = RecipeForm(self.request.POST,
                              self.request.FILES,
                              instance=self.object)
            if form.is_valid():
                self.object = form.save(commit=False)

        self.object.tags.clear()
        for tag in form.cleaned_data['tags']:
            self.object.tags.add(tag)

        self.object.save()
        return HttpResponseRedirect(self.get_success_url())



class RecipeDeleteView(UserPassesTestMixin, DeleteView):
    model = Recipe
    template_name = 'share_the_plate/recipe_confirm_delete.html'
    success_url = reverse_lazy('share_the_plate:recipe_list')

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user


class CustomLoginView(LoginView):
    """
    Custom login view.

    Inherits from LoginView provided by Django.
    """
    template_name = 'share_the_plate/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        """
        Sends user to profile once logged in.
        """
        if self.request.user is not None:
            return reverse_lazy('share_the_plate:profile_info',
                                kwargs={'username': self.request.user.username}
                                )
        return super().get_success_url()


def after_logout(request):
    return render(request, 'share_the_plate/after_logout.html')


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
            login(request,
                  user,
                  backend='django.contrib.auth.backends.ModelBackend')
            return redirect('share_the_plate:recipe_list')
        else:
            print(form.errors)  # print form errors if form is not valid
    else:
        form = SignUpForm()
    return render(request, 'share_the_plate/sign_up.html', {'form': form})


@login_required
def profile_info(request, username):
    """
    Display profile information of the user.

    :param request: HTTP request
    :param username: username of the user
    :return: Rendered profile information page
    """
    if request.user.username != username:
        return redirect('share_the_plate:index')
    user = User.objects.get(username=username)
    return render(request,
                  'share_the_plate/profile_info.html',
                  {'profile_user': user})


@login_required
def user_recipes(request, username):
    """
    Display submitted recipes of the user.

    :param request: HTTP request
    :param username: username of the user
    :return: Rendered list of users recipes page
    """
    if request.user.username != username:
        return redirect('share_the_plate:index')
    user = User.objects.get(username=username)
    user_recipes = Recipe.objects.filter(user=user)
    for recipe in user_recipes:
        recipe.featured_image_url = CloudinaryImage(str(recipe.featured_image)).build_url(crop="scale")
    return render(request,
                  'share_the_plate/user_recipes.html',
                  {'profile_user': user, 'user_recipes': user_recipes})


@login_required
def liked_recipes(request, username):
    """
    Display users liked recipes.

    :param request: HTTP request
    :param username: username of the user
    :return: Rendered list of users liked reciped page
    """
    if request.user.username != username:
        return redirect('share_the_plate:index')
    user = User.objects.get(username=username)
    likes = Like.objects.filter(user=user)
    return render(request,
                  'share_the_plate/liked_recipes.html',
                  {'profile_user': user, 'likes': likes})
