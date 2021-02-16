import ast

from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect

from api.models import Recipe, User


def index_view(request):
    # TODO фильтряация

    recipes = Recipe.objects.order_by('-pub_date').all()
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html',
                  {'page': page, 'paginator': paginator})


def profile_view(request, slug):
    # TODO фильтрация по тегам
    author = User.objects.get(username=slug)
    recipes = Recipe.objects.order_by('-pub_date').filter(author=author)
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'authorRecipe.html',
                  {'author': author, 'page': page, 'paginator': paginator})


# TODO follow, favorite, shoplist views
def follow_view(request):
    ...


def shopping_list_view(request):


    if request.method == 'POST':
        # We're getting a bytes type dictionary,
        # need to parse and convert it to a dictionary to extract
        # the needed recipe_id
        recipe_id = request.body
        recipe_id = recipe_id.decode('utf-8')
        recipe_id = ast.literal_eval(recipe_id)['id']

        user = User.objects.get(pk=request.user.id)
        shopping_list = user.shoplist.recipes.add(
            get_object_or_404(Recipe, id=recipe_id))
        return HttpResponse(status=200)

        # Added an if clause for additional clarity (I hope).

    user = User.objects.get(pk=request.user.id)
    shopping_list = user.shoplist.recipes.all()

    return render(request, 'shopList.html',
                  {'shopping_list': shopping_list})


def shopping_list_item_delete(request, id):
    # TODO сделать обновление страницы(проверить, нужно ли)
    user = User.objects.get(pk=request.user.id)
    user.shoplist.recipes.remove(get_object_or_404(Recipe, id=id))

    return HttpResponse(status=204)



def shopping_list_item_add(request, id):
    user = User.objects.get(pk=request.user.id)
    user.shoplist.recipes.add(Recipe.objects.get(id=id))


def shopping_list_download_view(request):
    # TODO
    ...

def favorite_recipe_view(request):
    # TODO
    ...
