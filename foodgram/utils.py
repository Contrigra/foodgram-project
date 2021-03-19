import itertools
import operator
from typing import Tuple

from api.models import Recipe


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
