from django.contrib import admin

from .models import Favorites
from .models import Ingredient
from .models import Recipe
from .models import RecipeIngredient
from .models import Shoplist
from .models import TimeTag


class RecipeIngredientInline(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    # TODO В списке рецептов вывести название и автора рецепта.
    # TODO Добавить фильтр по автору, названию рецепта, тегам.
    # TODO На странице рецепта вывести число добавлений этого рецепта в избранное.
    list_display = ['title', 'author', 'pub_date']
    inlines = (RecipeIngredientInline,)


@admin.register(TimeTag)
class TimeTagAdmin(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(Shoplist)
class ShoplistAdmin(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(Favorites)
class FavoritesAdmin(admin.ModelAdmin):
    search_fields = ('user',)
    list_filter = ('user',)
    empty_value_display = '-empty-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    search_fields = ('name',)


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient)
