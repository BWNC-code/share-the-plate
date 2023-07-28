from django.urls import path, reverse
from .views import (
    CustomLoginView,
    RecipeCreateView,
    RecipeUpdateView,
    RecipeDeleteView,
    home_page,
    signup,
    after_logout,
    recipe_list,
    recipe_detail,
    toggle_like,
    profile_info,
    user_recipes,
    liked_recipes,
    search,
)
from django.contrib.auth.views import LogoutView

app_name = "share_the_plate"

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("signup/", signup, name="signup"),
    path("recipes/", recipe_list, name="recipe_list"),
    path("recipe/new/", RecipeCreateView.as_view(), name="recipe_create"),
    path(
         "recipe/<slug:slug>/edit/",
         RecipeUpdateView.as_view(),
         name="recipe_edit"
        ),
    path(
        "recipe/<slug:slug>/delete/",
        RecipeDeleteView.as_view(),
        name="recipe_delete"
        ),
    path("recipe/<slug:slug>/", recipe_detail, name="recipe_detail"),
    path("toggle_like/<slug:slug>/", toggle_like, name="toggle_like"),
    path("profile/<str:username>/", profile_info, name="profile_info"),
    path("profile/<str:username>/recipes/", user_recipes, name="user_recipes"),
    path("profile/<str:username>/likes/", liked_recipes, name="liked_recipes"),
    path("search/", search, name="search"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("after-logout/", after_logout, name="after_logout"),
    path("", home_page, name="index"),
]
