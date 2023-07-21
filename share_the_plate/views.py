from django.shortcuts import render
from django.contrib.auth.views import LoginView


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


class CustomLoginView(LoginView):
    template_name = 'share_the_plate/login.html'
    redirect_authenticated_user = True