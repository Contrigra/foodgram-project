from django.contrib import admin
from .models import Ingredient
# Register your models here.


class IngredientAdmin(admin.ModelAdmin):
    # TODO customization
    pass

admin.site.register(Ingredient)