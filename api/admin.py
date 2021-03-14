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


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'pub_date']
    list_filter = ('author', 'title', 'tag')
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



admin.site.register(RecipeIngredient)
