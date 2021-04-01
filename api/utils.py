from api.models import RecipeIngredient, Ingredient


def save_RecipeIngredients(ingredients, recipe_pk):
    '''
    parse and create RecipeIngredients for manytomany relationship via the
    third model.
    :param ingredients: request.POST array with ingredient names in it for
    parsing and recipe_PK for database population
    :return: None
    '''

    for elem in ingredients:
        ingredient = Ingredient.objects.get(name__exact=elem['name'])
        obj = RecipeIngredient(recipe_id=recipe_pk, value=elem['value'],
                               ingredient_id=ingredient.pk)
        obj.save()


def edit_RecipeIngredients(ingredients, recipe_pk):
    """
    Parses ingredients and creates new recipe-ingredient relationships if
    there are new ingredients for a recipe
    :param ingredients: a list of ingredients in a receiving form
    :param recipe_pk: Recipe

    """

    for elem in ingredients:
        ingredient = Ingredient.objects.get(name__exact=elem['name'])
        obj = RecipeIngredient(recipe_id=recipe_pk, value=elem['value'],
                               ingredient_id=ingredient.pk)
        obj.save()


def populate_tags(request):
    """
    Returns a new request with updated request.POST with correctly populated
    tag data (space delimited string)
    """
    _choices = {'breakfast': 'breakfast',
                'lunch': 'lunch',
                'dinner': 'dinner'}

    _tag = ''
    for x in _choices:
        if x in request.POST:
            _tag += ' ' + _choices[x]
    post = request.POST.copy()
    post['tag'] = _tag
    request.POST = post

    return request


def get_tag_list(form):
    """
    A simple list of tags in a form of strings for proper render at the
    template level
    :param recipe form:
    :return a list of tags as strings:
    """
    _choices = {'breakfast': 'breakfast',
                'lunch': 'lunch',
                'dinner': 'dinner'}

    tags = []
    for tag in form.initial['tag']:
        if tag.slug in _choices:
            tags.append(_choices[tag.slug])

    return tags


def get_ingredients(data):
    ingredient_numbers = set()
    ingredients = []

    for key in data:
        if key.startswith('nameIngredient_'):
            _, number = key.split('_')
            ingredient_numbers.add(number)
    for number in ingredient_numbers:
        ingredients.append(
            {
                'name': data[f'nameIngredient_{number}'],
                'units': data[f'unitsIngredient_{number}'],
                'value': int(data[f'valueIngredient_{number}']),
                }
            )

    return ingredients
