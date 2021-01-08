from django.urls import path

from api.views import create_recipe_view, list_ingredients_view

urlpatterns = [
    path('create-recipe/', create_recipe_view, name='create_recipe'),
    path('create-recipe/ingredients', list_ingredients_view, name='list_ingredients')
]