from django.db import models

from users.models import User


class Dimension(models.Model):
    dimension = models.CharField(max_length=25, unique=True)


# TODO импорт фикстур

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

    # TODO связь с ингредиентом через другую модель
    class TimeTag(models.TextChoices):
        BREAKFAST = 'Завтрак'
        LUNCH = 'Обед'
        DINNGER = 'Ужин'

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    ingredients = models.ManyToManyField(Ingredient,
                                         blank=True,
                                         related_name='Ingredients',
                                         verbose_name='Ингредиенты')

    image = models.ImageField(upload_to='media/recipes', blank=True, null=True)
    tag = models.CharField(max_length=10, choices=TimeTag.choices,
                           default=TimeTag.BREAKFAST)
    time = models.IntegerField()
    slug = models.SlugField(unique=True)
    pub_date = models.DateTimeField('date published', auto_now_add=True,
                                    db_index=True)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
