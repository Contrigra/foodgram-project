import ast

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods

from api.models import Recipe, User
from foodgram.utils import sum_ingredients


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


@login_required
def shopping_list_view(request):
    if request.method == 'POST':
        recipe_id = request.body
        recipe_id = recipe_id.decode('utf-8')  # We receive a bytes type data
        recipe_id = ast.literal_eval(recipe_id)['id']

        user = User.objects.get(pk=request.user.id)
        shopping_list = user.shoplist.recipes.add(
            get_object_or_404(Recipe, id=recipe_id))

        data = {'success': True}
        return JsonResponse(data)

    user = User.objects.get(pk=request.user.id)
    shopping_list = user.shoplist.recipes.all()

    return render(request, 'shopList.html',
                  {'shopping_list': shopping_list})


@login_required
@require_http_methods('DELETE')
def shopping_list_item_delete(request, id):
    user = User.objects.get(pk=request.user.id)
    user.shoplist.recipes.remove(get_object_or_404(Recipe, id=id))

    data = {'success': True}
    return JsonResponse(data)


@login_required
def shopping_list_download_view(request):
    # TODO выдачу txt

    user = User.objects.get(pk=request.user.id)
    ingredient_list = list(user.shoplist.recipes.values('ingredients__name',
                                                        'recipeingredient__value',
                                                        'ingredients__units'))
    ingredient_list = sum_ingredients(ingredient_list)
    print(ingredient_list)

    return HttpResponse(200)


def favorite_recipe_view(request):
    # TODO
    ...


# TODO follow
def follow_view(request):
    ...
