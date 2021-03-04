import ast

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse, FileResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_http_methods

from api.models import Recipe
from foodgram.utils import sum_ingredients, get_tags
from users.models import User, Follow


def index_view(request):
    # TODO фильтряация
    # TODO https://stackoverflow.com/questions/223990/how-do-i-perform-query-filtering-in-django-templates
    # ?tags= название параметра, автоматический рендер в ХТМЛ и добавление его в урл
    tags = get_tags(request)
    if tags is None:
        recipes = Recipe.objects.order_by('-pub_date').all()
    else:
        recipes = Recipe.objects.order_by('-pub_date').filter(tag__name__in=tags)
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html',
                  {'page': page, 'paginator': paginator})


def profile_view(request, slug):
    # TODO фильтрация по тегам
    author = User.objects.get(username=slug)
    recipes = Recipe.objects.order_by('-pub_date').filter(author=author)
    subscribed = (request.user.follower.select_related('author').filter(
        author=author).exists())


    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'authorRecipe.html',
                  {'author': author, 'page': page, 'paginator': paginator,
                   'subscribed': subscribed})


@login_required
def shopping_list_view(request):
    if request.method == 'POST':
        recipe_id = request.body
        recipe_id = recipe_id.decode('utf-8')  # We receive a bytes type data
        recipe_id = ast.literal_eval(recipe_id)['id']

        user = User.objects.get(pk=request.user.id)
        user.shoplist.recipes.add(get_object_or_404(Recipe, id=recipe_id))

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
    user = User.objects.get(pk=request.user.id)
    ingredient_list = list(user.shoplist.recipes.values('ingredients__name',
                                                        'recipeingredient__value',
                                                        'ingredients__units'))
    ingredient_list = sum_ingredients(ingredient_list)
    with open(f'{user.username}_shopping_list.txt', 'w+',
              encoding='utf-8') as txt:
        for ingredient in ingredient_list:
            txt.write('{d} {v}{u}\n'.format(d=ingredient['ingredients__name'],
                                            v=ingredient[
                                                'recipeingredient__value'],
                                            u=ingredient[
                                                'ingredients__units']))

        return FileResponse(open(txt.name, 'rb'), as_attachment=True)


@login_required
def favorite_recipe_view(request):
    if request.method == 'POST':
        recipe_id = request.body
        recipe_id = recipe_id.decode('utf-8')  # We receive a bytes type data
        recipe_id = ast.literal_eval(recipe_id)['id']

        user = User.objects.get(pk=request.user.id)
        user.favorites.recipes.add(get_object_or_404(Recipe, id=recipe_id))

        data = {'success': True}
        return JsonResponse(data)

    user = User.objects.get(pk=request.user.id)
    recipes = user.favorites.recipes.all().order_by('-pub_date')
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'favorite.html',
                  {'page': page, 'paginator': paginator})


@login_required
@require_http_methods('DELETE')
def favorite_item_delete(request, id):
    user = User.objects.get(pk=request.user.id)
    user.favorites.recipes.remove(get_object_or_404(Recipe, id=id))

    data = {'success': True}
    return JsonResponse(data)


# TODO follow
@login_required
def subscriptions_index(request):
    user = request.user
    followed_authors = user.follower.select_related('author').order_by(
        '-author')
    paginator = Paginator(followed_authors, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'myFollow.html',
                  {'page': page, 'paginator': paginator,
                   'followed_authors': followed_authors})


@login_required
def follow_view(request, id):
    author = get_object_or_404(User, id=id)
    data = {'success': True}

    if request.user != author:
        follow, created = Follow.objects.get_or_create(user=request.user,
                                                       author=author)
        if created:
            return JsonResponse(data)

    return redirect('profile', slug=author.username)


@login_required
def unfollow_view(request, id):
    # TODO кнопку отписаться из страницы подписок
    author = get_object_or_404(User, id=id)
    follow_to_delete = Follow.objects.get(user=request.user,
                                          author=author)
    if follow_to_delete is not None:
        follow_to_delete.delete()
        data = {'success': True}

        return JsonResponse(data)

    return redirect('profile', slug=author.username)
