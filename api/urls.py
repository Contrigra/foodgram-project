from django.urls import path

from api.views import create_recipe_view, list_ingredients_view, single_recipe_view

# TODO single page view of a recipe
urlpatterns = [
    path('create-recipe/', create_recipe_view, name='create_recipe'),
    path('create-recipe/ingredients', list_ingredients_view,
         name='list_ingredients'),
    path('<slug:slug>', single_recipe_view, name='single_recipe')
]