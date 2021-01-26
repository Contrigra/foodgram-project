from api.models import RecipeIngredient, Ingredient


def get_and_save_RecipeIngredients(ingredients, recipe_pk):
    '''
    parse and create RecipeIngredients for manytomany relationship via the third model.
    :param ingredients: request.POST array with ingredient names in it for parsing and recipe_PK for database population
    :return: None
    '''

    arr = []
    i = 1
    for ingredient in ingredients.keys():
        print(ingredient.startswith('name'))
        if ingredient.startswith('name'):
            arr.append([ingredients[ingredient], ingredients[f'valueIngredient_{i}']])
            i += 1

    for name, value in arr:
        ingredient = Ingredient.objects.get(name__exact=name)
        obj = RecipeIngredient(recipe_id=recipe_pk, value=value,
                                              ingredient_id=ingredient.pk)
        obj.save()



