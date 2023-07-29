from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.db.models import Q, Prefetch
from ..models import Recipe, Comment, Like, Category
from .forms import RecipeForm, CommentForm


@login_required
def toggle_like(request, slug):
    user = request.user
    recipe = get_object_or_404(Recipe, slug=slug)
    like, created = Like.objects.get_or_create(user=user, recipe=recipe)

    if created:
        action = "like"
        messages.success(request, f"You have liked {recipe.title}.")
    else:
        action = "unlike"
        like.delete()
        messages.success(request, f"You have unliked {recipe.title}.")

    return redirect("share_the_plate:recipe_detail", slug=slug)


def recipe_list(request):
    """
    List the 10 most recent recipes.

    :param request: HTTP request
    :return: Rendered list of recipes
    """
    main_recipe = Recipe.objects.filter(status=1).order_by('-created_at').first()
    categories = Category.objects.all()

    category_recipes = []
    for category in categories:
        recipes = Recipe.objects.filter(status=1, categories=category).order_by('-created_at')[:3]
        category_recipes.append((category, recipes))

    context = {'main_recipe': main_recipe, 'category_recipes': category_recipes}

    return render(request, 'share_the_plate/recipe_list.html', context)


def recipe_detail(request, slug):
    """
    Display the detail of a specific recipe.

    :param request: HTTP request
    :param slug: Slug of the recipe
    :return: Rendered detail view of the recipe
    """
    recipe = get_object_or_404(Recipe, slug=slug)
    comments = Comment.objects.filter(recipe=recipe)
    new_comment = None
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.recipe = recipe
            new_comment.user = request.user
            new_comment.save()
    else:
        comment_form = CommentForm()

    # Check if the recipe is already liked by the user
    user_has_liked = False
    if request.user.is_authenticated:
        if Like.objects.filter(user=request.user, recipe=recipe).exists():
            user_has_liked = True

    return render(
        request,
        "share_the_plate/recipe_detail.html",
        {
            "recipe": recipe,
            "comments": comments,
            "new_comment": new_comment,
            "comment_form": comment_form,
            "user_has_liked": user_has_liked,
        },
    )


class RecipeCreateView(LoginRequiredMixin, CreateView):
    """
    Display a form dor creating a new recipe.
    Only accessed by authenticated user so can set author.
    Inherits LoginRequiredMixin to check user is logged in.
    Inherits from CreateView for the creation process.
    """

    model = Recipe
    form_class = RecipeForm
    template_name = "share_the_plate/recipe_form.html"

    def form_valid(self, form):
        """
        Set the current user as the author of the recipe before saving.
        :param form: Recipe creation form
        :return: HTTP response
        """
        form.instance.user = self.request.user
        response = super().form_valid(form)
        form.instance.tags.add(*self.request.POST.get("tags").split(","))
        return response

    def form_invalid(self, form):
        """
        Overwrite the form_invalid method to include a message.
        """
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        return super().form_invalid(form)


class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = "share_the_plate/recipe_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user

    def get_login_url(self):
        if not self.request.user.is_authenticated:
            return super().get_login_url()
        else:
            return reverse(
                "share_the_plate:recipe_detail",
                kwargs={"slug": self.get_object().slug}
            )

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if self.request.method == "POST":
            form = RecipeForm(
                self.request.POST, self.request.FILES, instance=self.object
            )
            if form.is_valid():
                self.object = form.save(commit=False)

        self.object.tags.clear()
        for tag in form.cleaned_data["tags"]:
            self.object.tags.add(tag)

        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class RecipeDeleteView(UserPassesTestMixin, DeleteView):
    model = Recipe
    template_name = "share_the_plate/recipe_confirm_delete.html"
    success_url = reverse_lazy("share_the_plate:user_recipes")

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user


def search(request):
    query = request.GET.get("q")
    if query:
        results = Recipe.objects.filter(
            Q(title__icontains=query)
            | Q(ingredients__icontains=query)
            | Q(tags__name__icontains=query)
        ).distinct()
    else:
        results = Recipe.objects.none()
    return render(request,
                  "share_the_plate/search_results.html",
                  {"results": results}
                  )
