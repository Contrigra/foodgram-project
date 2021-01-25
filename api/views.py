from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from slugify import slugify

from api.models import Ingredient, Recipe, RecipeIngredient
from .forms import RecipeForm, RecipeIngredientForm


@login_required
def create_recipe_view(request):
    """
    View function for a recipe creation page. Parses tags from checkboxes
    input, prepares the data for the tag field.
    """
    _choices = {'breakfast': 'breakfast',
                'lunch': 'lunch',
                'dinner': 'dinner'}

    if request.method == 'POST':
        # transforming received tag checkbox to acceptable (
        # space-delimited string) input for the form and modify POST request
        # to include acceptable field data.

        # Should I create another function for this or this is acceptable
        # since it's the necessary part of the recipe creation? And will be
        # used only here?

        _tag = ''
        for x in _choices:
            if x in request.POST:
                _tag += ' ' + _choices[x]
        post = request.POST.copy()
        post['tag'] = _tag
        request.POST = post

        ingredient_form = RecipeIngredientForm(request.POST or None)
        form = RecipeForm(request.POST or None, request.FILES or None)

# TODO адаптировать данные ингредиентов и форму.
        if form.is_valid() and ingredient_form.is_valid():
            recipe = form.save(commit=False)
            recipe_ingredients = ingredient_form.save(commit=False)
            recipe.author = request.user
            recipe.slug = slugify(recipe.title, only_ascii=True)
            recipe_ingredients.recipe = recipe
            recipe.save()
            # This line is needed to save the tags.
            form.save_m2m()

            # TODO redirect to the single page of the recipe
            return redirect(to='/', username=request.user.username,
                            permanent=True)

    form = RecipeForm()
    ingredient_form = RecipeIngredientForm()

    return render(request, 'formRecipe.html', {'form': form, 'ingredient_form': ingredient_form})


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

# TODO сделать страницу
def single_recipe_view(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    recipe_ingredients = recipe.ingredients.all()
    print(recipe_ingredients)
    return render(request, 'singlePage.html', {'slug':slug, 'recipe': recipe })

