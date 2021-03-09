import itertools
import operator

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


def get_url_with_types(request):
    url_type_line = request.GET.get('type')
    return url_type_line


def get_filter_type(request):
    try:
        given_types = list(request.GET.get('type'))
    except TypeError:
        given_types = None
    return given_types


def get_types(data):
    types_list = []
    for key in data:
        if key != 'picture' and key != 'picture-clear':
            if data[key] == 'on':
                types_list.append(key)
    return types_list

