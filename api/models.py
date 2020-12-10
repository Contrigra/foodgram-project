from django.db import models

from users.models import User


class Ingredient(models.Model):
    """
    The ingredient model for recipes
    """

    title = models.CharField(max_length=256)
    measure = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return f'{self.title}, {self.measure}'


class Recipe(models.Model):
    """
    The recipe model, ingredients field is connected to Ingredient model.
    With a subclass of tags
    """

    class TimeTag(models.TextChoices):
        BREAKFAST = 'Завтрак'
        LUNCH = 'Обед'
        DINNER = 'Ужин'

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    ingredients = models.ManyToManyField(Ingredient,
                                         through='RecipeIngredient',
                                         blank=True,
                                         related_name='ingredients',
                                         verbose_name='Ингредиенты')

    image = models.ImageField(upload_to='media/recipes', blank=True, null=True)
    tag = models.CharField(max_length=10, choices=TimeTag.choices,
                           default=TimeTag.BREAKFAST)
    cooking_time = models.IntegerField()

    # TODO slug, оставить?
    slug = models.SlugField(unique=True)
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
    amount = models.IntegerField()
