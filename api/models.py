from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from taggit.managers import TaggableManager
from taggit.models import TagBase, GenericTaggedItemBase

User = get_user_model()


class Ingredient(models.Model):
    """
    The ingredient model for recipes
    """

    name = models.CharField(max_length=256)
    units = models.CharField(max_length=64, blank=True)

    class Meta:
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'
        ordering = ['name']

    def __str__(self):
        return f'{self.name}, {self.units}'


class TimeTag(TagBase):
    """
    Tag model for recipe types
    """

    colour = models.CharField(max_length=256)
    ru_local = models.CharField(max_length=64)

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'TimeTags'


class RecipeTag(GenericTaggedItemBase):
    tag = models.ForeignKey(TimeTag, on_delete=models.CASCADE,
                            related_name='%(app_label)s_%(class)s_items')


class Recipe(models.Model):
    """
    The recipe model, ingredients field is connected to Ingredient model.
    Tag field uses built in features of Taggit library
    and extended model TimeTag
    """

    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='recipes')
    title = models.CharField(max_length=256, unique=True)
    ingredients = models.ManyToManyField(Ingredient,
                                         through='RecipeIngredient',
                                         related_name='ingredients',
                                         verbose_name='Ингредиенты',
                                         blank=True
                                         )

    image = models.ImageField(upload_to='recipes')
    tag = TaggableManager(through=RecipeTag)

    time = models.PositiveSmallIntegerField(
        null=False,
        validators=[MinValueValidator
                    (1, message='Время должно быть равно 1 или более минут')],
        help_text='Укажите время '
                  'в минутах',
        default=10)

    slug = models.SlugField(unique=True, max_length=256)
    pub_date = models.DateTimeField('date published', auto_now_add=True,
                                    db_index=True)
    description = models.TextField()

    class Meta:
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.title


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, null=True,
                                   on_delete=models.SET_NULL)
    value = models.PositiveSmallIntegerField(
        verbose_name='ingredient weight', null=False,
        validators=[MinValueValidator(1)], default=10,
        help_text='Добавьте необходимое количество ингредиентов'

        )

    class Meta:
        verbose_name = 'Recipe Ingredient'
        verbose_name_plural = 'Recipe Ingredients'

        constraints = [
            models.UniqueConstraint(fields=('recipe', 'ingredient',),
                                    name='Unique Ingredients')
            ]

    def __str__(self):
        return f'{self.recipe.title} - {self.ingredient.name} ' \
               f'{self.value} {self.ingredient.units},'


class Shoplist(models.Model):
    """ A user's shopping list"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True,
                                null=True)
    recipes = models.ManyToManyField(Recipe, blank=True)

    def __str__(self):
        return f'{self.user} shopping list'

    class Meta:
        verbose_name = 'Shopping List'
        verbose_name_plural = 'Shopping Lists'


class Favorites(models.Model):
    """A list of a user's favored recipes"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True,
                                null=True)
    recipes = models.ManyToManyField(Recipe, blank=True)

    def __str__(self):
        return f'{self.user} favourites list'

    class Meta:
        verbose_name = 'Favorite list'
        verbose_name_plural = 'Favorite lists'
