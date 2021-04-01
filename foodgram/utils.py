import itertools
import operator

from django.contrib.auth import get_user_model

from api.models import Recipe


def obtain_recipes(request, received_tags):
    """
    Parses request and returns a proper recipe list. There are three cases,
    one is for index page, the second one is for profile pagem, and the third
    one for favourites
    :param request:
    :param received_tags: A list of string tag PKs
    :return: a recipes queryset
    """
    # for profile
    try:
        slug = request.resolver_match.kwargs['slug']
    except KeyError:
        slug = None
    if slug is not None:
        User = get_user_model()
        author = User.objects.get(username=slug)
        recipes = Recipe.objects.filter(
            tag__id__in=received_tags, author=author).distinct()
    # for favorites
    elif request.resolver_match.url_name == 'favorites':
        User = get_user_model()
        user = User.objects.get(pk=request.user.id)
        recipes = user.favorites.recipes.all().filter(
            tag__id__in=received_tags).distinct()
    # for index
    else:
        recipes = Recipe.objects.filter(
            tag__id__in=received_tags).distinct()

    return recipes


def sum_ingredients(ingredient_list):
    key = operator.itemgetter('ingredients__name', 'ingredients__units')

    ingredient_list = [{'recipeingredient__value': sum(
        x['recipeingredient__value'] for x in g),
        'ingredients__name': k[0],
        'ingredients__units': k[1]}
        for k, g in
        itertools.groupby(sorted(ingredient_list, key=key),
                          key=key)]
    return ingredient_list


def get_url_with_tags(request):
    url_tags_line = request.GET.get('tags')
    return url_tags_line


def get_filter_tags(request):
    try:
        given_tags = list(request.GET.get('tags'))
    except TypeError:
        given_tags = None
    return given_tags


def get_tags(data):
    tags_list = []
    for key in data:
        if key != 'picture' and key != 'picture-clear':
            if data[key] == 'on':
                tags_list.append(key)
    return tags_list


def get_tag_status(recipes) -> bool:
    if not recipes:
        no_tags = True
    else:
        no_tags = False

    return no_tags
