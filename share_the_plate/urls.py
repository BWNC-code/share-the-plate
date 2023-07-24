from django.urls import path
from . import views
from .views import CustomLoginView

app_name = 'share_the_plate'

urlpatterns = [
    path('', views.home_page, name='index'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('signup/', views.signup, name='signup'),
    path('recipes/', views.recipe_list, name='recipe_list'),
    path('recipe/<slug:slug>/', views.recipe_detail, name='recipe_detail'),
    path('profile/<str:username>/', views.profile, name='profile')
]