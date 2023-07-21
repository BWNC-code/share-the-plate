"""django_share_the_plate URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from share_the_plate import views
from share_the_plate.views import CustomLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('share_the_plate.urls')),  # include app's urls
    path('recipes/', views.recipe_list, name='recipe_list'),
    path('login/', CustomLoginView.as_view(), name='login')  # The login page

]
