from django.urls import path

from . import views

# TODO move templates into the app folder.
urlpatterns = [
    path('create-recipe/', views.create_recipe_view, name='create_recipe'),
    path('create-recipe/ingredients', views.list_ingredients_view,
         name='list_ingredients'),
    path('<slug:slug>', views.single_recipe_view, name='single_recipe'),
    path('<slug:slug>/edit', views.recipe_edit_view, name='recipe_edit'),

]