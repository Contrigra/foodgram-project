from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet

from users.models import Follow
from .models import Favorites
from .models import Ingredient
from .models import Recipe
from .models import RecipeIngredient
from .models import Shoplist
from .models import TimeTag


class RecipeIngredientInlineFormSet(BaseInlineFormSet):
    """ Validation for the RecipeIngredientInline,
    all recipes require at least one ingredient"""

    def clean(self):
        # self.cleaned_data is a bit dirty,
        # It somehow sends an empty dictionary
        # if the admin does not put any value in an empty inline
        not_for_delete = []
        for inline in self.cleaned_data:
            if bool(inline) is True:
                if inline['DELETE'] is False:
                    not_for_delete.append(inline)

        if len(not_for_delete) == 0:
            raise ValidationError(
                ('Recipe requires at least one ingredient'))


class RecipeIngredientInline(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1
    formset = RecipeIngredientInlineFormSet


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    search_fields = ('author__username', 'title', 'tag__name')
    list_display = ['title', 'author', 'pub_date']
    readonly_fields = ('favorites_count',)
    list_filter = ('author', 'title', 'tag')
    inlines = (RecipeIngredientInline,)

    def favorites_count(self, obj):
        count = Favorites.objects.filter(recipes=obj).count()
        return count


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


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    search_fields = ('author__username', 'user__username',)


admin.site.register(RecipeIngredient)
