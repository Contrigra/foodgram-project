from api.models import RecipeIngredient, Ingredient


def get_and_save_RecipeIngredients(ingredients, recipe_pk):
    '''
    parse and create RecipeIngredients for manytomany relationship via the
    third model.
    :param ingredients: request.POST array with ingredient names in it for
    parsing and recipe_PK for database population
    :return: None
    '''

    arr = []
    for ingredient in ingredients.keys():
        if ingredient.startswith('nameIngredient_'):
            _, i = ingredient.split('_')
            arr.append(
                [ingredients[ingredient], ingredients[f'valueIngredient_{i}']])

    for name, value in arr:
        ingredient = Ingredient.objects.get(name__exact=name)
        obj = RecipeIngredient(recipe_id=recipe_pk, value=value,
                               ingredient_id=ingredient.pk)
        obj.save()


def populate_tags(request):
    """
    Returns a new request with updated request.POSt with correctly populated
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
