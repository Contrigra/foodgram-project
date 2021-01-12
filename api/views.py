from django.shortcuts import render
from .forms import RecipeForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from api.models import Ingredient
from api.models import Recipe
from django.db.models import F
from urllib.parse import unquote
from django.http import HttpResponse
from django.http import JsonResponse



@login_required
def create_recipe_view(request):
    """
    View function for a recipe creation page
    """

    if request.method == 'POST':
        form = RecipeForm(request.POST or None, files=request.FILES or None)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            return reverse('index')
    form = RecipeForm()

    return render(request, 'formRecipe.html', {'form': form})


def list_ingredients_view(request):
    """
    Autofill for a dropdown field of ingredients for recipe creation form
    """
    # TODO проверить, работает ли istartswith с postgreSQL корректно.
    #  MySQL, вроде не работает не с ASCII символами

    text = request.GET.get('query')
    ingredients = list(Ingredient.objects.filter(
        title__istartswith=text).values('title', 'measure'))
    return JsonResponse(ingredients, safe=False)