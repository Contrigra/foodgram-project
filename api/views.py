from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from slugify import slugify

from api.models import Ingredient, Recipe, RecipeIngredient
from users.models import User
from .forms import RecipeForm
from .utils import save_RecipeIngredients, populate_tags, \
    get_tag_list, get_ingredients


@login_required
def create_recipe_view(request):
    """
    View function for a recipe creation page. Parses tags from checkboxes
    input, prepares the data for the tag field.
    """

    if request.method == 'POST':

        request = populate_tags(request)
        form = RecipeForm(request.POST or None, request.FILES or None)

        # You need at least one ingredient
        ingredients = get_ingredients(request.POST)
        if not ingredients:
            form.add_error(None,
                           ValidationError(
                               'Add at least one ingredient'))

        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.slug = slugify(recipe.title)
            recipe.save()
            form.save_m2m()
            # due to intermediary model for many-to-many relationship of a
            # Recipe and Ingredients, you have to manually create objects of
            # the said third model.
            try:
                save_RecipeIngredients(ingredients, recipe_pk=recipe.pk)

            except IntegrityError:
                recipe_form = RecipeForm(request.POST or None,
                                         files=request.FILES,
                                         instance=recipe)
                data = {'form': recipe_form,
                        'message': 'Нельзя создать с рецепт с двумя'
                                   ' одинаковыми ингредиентами',
                        'ingredient_error': True, 'recipe': recipe}

                recipe.delete()
                return render(request, 'recipe/recipe_form.html', data)

            return redirect(to='single_recipe',
                            permanent=True, slug=recipe.slug)

        else:
            return render(request, 'recipe/recipe_form.html', {'form': form, })

    form = RecipeForm()
    return render(request, 'recipe/recipe_form.html', {'form': form, })


def list_ingredients_view(request):
    """
    Autofill for a dropdown field of ingredients for recipe creation form
    """

    text = request.GET.get('query')
    ingredients = list(Ingredient.objects.filter(
        name__istartswith=text).values('name', 'units'))

    return JsonResponse(ingredients, safe=False)


def single_recipe_view(request, slug):
    """
    Renders out a single page recipe page. Obtaining tags and list of
    ingredients of M2M relationship and passing it to the template.
    """
    recipe = get_object_or_404(Recipe, slug=slug)
    recipe_ingredients = RecipeIngredient.objects.filter(recipe=recipe)
    tags = recipe.tag.names()
    data = {
        'slug': slug,
        'recipe': recipe,
        'recipe_ingredients': recipe_ingredients,
        'tags': tags, }
    if request.user.is_authenticated:
        subscribed = (request.user.follower.select_related('author').filter(
            author=recipe.author).exists())
        data['subscribed'] = subscribed

    return render(request, 'recipe/recipe_singlePage.html', data)


@login_required
def recipe_edit_view(request, slug):
    """
    View function for a recipe edit page. Parses tags from checkboxes
    input, prepares the data for the tag field. Ingredient validation
    """

    recipe = get_object_or_404(Recipe, slug=slug)
    author = get_object_or_404(User, username=recipe.author)
    if request.user != author:
        return redirect("single_recipe",
                        slug=slug)

    request = populate_tags(request)
    form = RecipeForm(request.POST or None, files=request.FILES or None,
                      instance=recipe)

    current_recipe_ingredients = RecipeIngredient.objects.filter(recipe=recipe)
    current_recipe_tags = recipe.tag.all()
    tags = get_tag_list(form)
    if request.method == "POST":
        ingredients = get_ingredients(request.POST)
        if not ingredients:
            form.add_error(None,
                           ValidationError(
                               'Требуется хотя бы один ингредиент'))
        if form.is_valid():

            current_recipe_ingredients.delete()
            current_recipe_tags.delete()

            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.slug = slugify(recipe.title)
            recipe.save()
            form.save_m2m()

            try:
                save_RecipeIngredients(ingredients, recipe_pk=recipe.pk)

            except IntegrityError:
                recipe_form = form

                recipe_ingredients = RecipeIngredient.objects.filter(
                    recipe=recipe)

                data = {'form': recipe_form,
                        'message': 'Нельзя создать с рецепт с двумя'
                                   ' одинаковыми ингредиентами', 'edit': True,
                        'ingredient_error': True, 'recipe': recipe,
                        'tags': tags, 'recipe_ingredients': recipe_ingredients}

                return render(request, 'recipe/recipe_form.html', data)

            return redirect(to='single_recipe',
                            permanent=True, slug=recipe.slug)

    recipe_ingredients = RecipeIngredient.objects.filter(recipe=recipe)
    data = {'form': form, 'recipe': recipe, 'edit': True,
            'recipe_ingredients': recipe_ingredients, 'tags': tags}

    return render(
        request, "recipe/recipe_form.html", data
        )


def delete_recipe_view(request, slug):
    """
    Deletes recipe and its ingredients and redirects to index page
    """

    recipe = get_object_or_404(Recipe, slug=slug)
    ingredients = RecipeIngredient.objects.filter(recipe=recipe)
    recipe.delete()

    # Deleting RecipeIngredients since they're unreachable from recipe object
    ingredients.delete()

    return redirect(to='index')
