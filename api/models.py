from django.core.validators import MinValueValidator
from django.db import models
from taggit.managers import TaggableManager
from users.models import User


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


class TimeTag(models.Model):
    breakfast = models.BooleanField(default=False, verbose_name='Завтрак')
    lunch = models.BooleanField(default=False, verbose_name='Обед')
    dinner = models.BooleanField(default=False, verbose_name='Ужин')


# TODO снести базу и сделать по новой импротировав все данные из фикстур

class Recipe(models.Model):
    """
    The recipe model, ingredients field is connected to Ingredient model.
    With a subclass of tags
    """

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=256, unique=True)
    ingredients = models.ManyToManyField(Ingredient,
                                         through='RecipeIngredient',
                                         blank=True,
                                         related_name='ingredients',
                                         verbose_name='Ингредиенты')

    image = models.ImageField(upload_to='recipes', blank=True, null=True)
    tag = TaggableManager()

    time = models.PositiveSmallIntegerField(null=True, blank=True)

    slug = models.SlugField(unique=True, max_length=256)
    pub_date = models.DateTimeField('date published', auto_now_add=True,
                                    db_index=True)
    description = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    value = models.PositiveSmallIntegerField(
        verbose_name='ingredient weight', null=False,
        validators=[MinValueValidator(1)], default=10,
        help_text='Добавьте необходимое количество ингредиентов'
    )
