from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from api.models import Ingredient
from .forms import RecipeForm
from slugify import slugify


@login_required
def create_recipe_view(request):
    """
    View function for a recipe creation page
    """
    _choices = {'breakfast': 'breakfast',
               'lunch': 'lunch',
               'dinner': 'dinner'}

    if request.method == 'POST':
        # transforming received tag checkbox to acceptable input for the form
        # Should I create another function for this or this is acceptable
        # since it's the necessary part of recipe creation? Requires a
        # space delimited string
        _tag = ''
        for x in _choices:
            if x in request.POST:
                _tag += ' ' + _choices[x]

        print(_tag)
        post = request.POST.copy()
        post['tag'] = _tag

        request.POST = post
        form = RecipeForm(request.POST or None, files=request.FILES or None)


        # TODO сделать загрузку картинок и времени тэги
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.slug = slugify(recipe.title, only_ascii=True)
            recipe.save()
            # This line is needed to save the tags.
            form.save_m2m()

            return redirect(to='/', username=request.user.username,
                            permanent=True)



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
        title__istartswith=text).values('title', 'measure'))
    return JsonResponse(ingredients, safe=False)
