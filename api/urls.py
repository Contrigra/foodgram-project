from django.urls import path

from api.views import create_recipe_view

urlpatterns = [
    path('create-recipe/', create_recipe_view, name='create_recipe'),
]