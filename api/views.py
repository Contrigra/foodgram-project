from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse

from api.models import Ingredient
from .forms import RecipeForm


@login_required
def create_recipe_view(request):
    """
    View function for a recipe creation page
    """
    choices = {'breakfast': 'breakfast',
               'lunch': 'lunch',
               'dinner': 'dinner'}
    # TODO сделать, чтобы работал TAG, Завтрак, обед, ужин.
    # TAG не высылается
    #


    if request.method == 'POST':

        tag = []
        for x in request.POST:
            if x in choices:
                tag.append(choices[x])

        post = request.POST.copy()
        post['tag'] = tag
        request.POST = post

        print(request.POST)

        form = RecipeForm(request.POST or None, files=request.FILES or None)



        print(request.POST)

        # TODO посмотреть какие есть опции выбора
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            return reverse('index')

        print(form.errors)

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
