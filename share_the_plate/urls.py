from django.urls import path
from . import views
from .views import CustomLoginView, RecipeCreateView, RecipeUpdateView
from django.contrib.auth.views import LogoutView

app_name = 'share_the_plate'

urlpatterns = [
    path('', views.home_page, name='index'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('signup/', views.signup, name='signup'),
    path('recipes/', views.recipe_list, name='recipe_list'),
    path('recipe/new/', RecipeCreateView.as_view(), name='recipe_create'),
    path('recipe/<int:pk>/edit/', RecipeUpdateView.as_view(), name='recipe_edit'),
    path('recipe/<slug:slug>/', views.recipe_detail, name='recipe_detail'),
    path('profile/<str:username>/', views.profile_info, name='profile_info'),
    path('profile/<str:username>/recipes/', views.user_recipes, name='user_recipes'),
    path('profile/<str:username>/likes/', views.liked_recipes, name='liked_recipes'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('after-logout/', views.after_logout, name='after_logout')
]