from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from slugify import slugify

from api.models import Ingredient, Recipe, RecipeIngredient, User
from .forms import RecipeForm
from .utils import get_and_save_RecipeIngredients, populate_tags, \
    get_tag_list


@login_required
def create_recipe_view(request):
    """
    View function for a recipe creation page. Parses tags from checkboxes
    input, prepares the data for the tag field.
    """

    if request.method == 'POST':

        request = populate_tags(request)
        form = RecipeForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.slug = slugify(recipe.title, only_ascii=True)

            recipe.save()
            form.save_m2m()
            # due to intermediatory model for many-to-many relationship of a
            # Recippe and Ingredients, you have to manually create objects of
            # the said third model.
            get_and_save_RecipeIngredients(request.POST, recipe_pk=recipe.pk)

            return redirect(to='single_recipe',
                            permanent=True, slug=recipe.slug)

    form = RecipeForm()

    return render(request, 'formRecipe.html', {'form': form, })


def list_ingredients_view(request):
    """
    Autofill for a dropdown field of ingredients for recipe creation form
    """
    # TODO проверить, работает ли istartswith с postgreSQL корректно.
    #  MySQL, вроде не работает не с ASCII символами

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

    return render(request, 'singlePage.html', {
        'slug': slug,
        'recipe': recipe,
        'recipe_ingredients': recipe_ingredients,
        'tags': tags, })


# TODO make form populated with saved data. Make proper rendering in the HTML template

@login_required
def recipe_edit_view(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    author = get_object_or_404(User, username=recipe.author)
    edit = True

    # Only the owner should have the permission to edit a recipe
    if request.user != author:
        return redirect("single_recipe",
                        slug=slug)

    request = populate_tags(request)
    form = RecipeForm(request.POST or None, files=request.FILES or None,
                      instance=recipe)

    # Get a list of tags for proper tag rendering at the template level
    tags = get_tag_list(form)

    if request.method == "POST":
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.slug = slugify(recipe.title, only_ascii=True)
            recipe.save()
            form.save_m2m()
            # due to intermediatory model for many-to-many relationship of a
            # Recipe and Ingredients, you have to manually create objects of
            # the said third model.
            get_and_save_RecipeIngredients(request.POST, recipe_pk=recipe.pk)

            return redirect(to='single_recipe',
                            permanent=True, slug=recipe.slug)

    recipe_ingredients = RecipeIngredient.objects.filter(recipe=recipe)

    return render(
        request, "formRecipe.html",
        {'form': form, 'recipe': recipe, 'edit': edit,
         'recipe_ingredients': recipe_ingredients, 'tags': tags},
    )


def delete_recipe_view(request, slug):
    """
    Deletes recipe and its ingredients and redirects to index page
    """

    recipe = get_object_or_404(Recipe, slug=slug)
    ingredients = RecipeIngredient.objects.filter(recipe=recipe)
    recipe.delete()
    ingredients.delete()

    return redirect(to='index')

    # Deleting RecipeIngredients since they're unreachable from recipe object
