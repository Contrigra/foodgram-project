from django.forms import ModelMultipleChoiceField, ModelForm, \
    CheckboxSelectMultiple

from .models import Recipe, RecipeIngredient


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ('title', 'image', 'tag', 'time', 'ingredients',
                  'description')

