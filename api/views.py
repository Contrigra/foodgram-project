from django.shortcuts import render
from .forms import RecipeForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from api.models import Ingredient
from api.models import Recipe
from django.db.models import F

from django.http import HttpResponse
from django.http import JsonResponse
@login_required
def create_recipe_view(request):
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
    # TODO вытащить из queryset тайтл и в чём измеряется
    # TODO или же переделать немного api? Может там ждутся другие аргументы?
    text = request.GET.get('query')
    ingredients = list(Ingredient.objects.filter(
        title__istartswith=text).values(
        name=F('title'), dimension=F('measure')))
    return JsonResponse(ingredients, safe=False)