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