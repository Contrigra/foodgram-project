from django.forms import ModelMultipleChoiceField, ModelForm, \
    CheckboxSelectMultiple

from .models import Recipe, TimeTag

class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ('title', 'ingredients', 'image', 'tag', 'time',
                  'description')
