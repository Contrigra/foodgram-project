from django.core.paginator import Paginator
from django.shortcuts import render

from api.models import Recipe, User, Shoplist


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
    # TODO удаление предмета из шоплиста и скачать список в .txt, посчитать
    user = User.objects.get(pk=request.user.id)
    shopping_list = user.shoplist.recipes.all()

    return render(request, 'shopList.html', {'shopping_list' : shopping_list})

def favorite_recipe_view(request):
    ...