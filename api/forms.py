from django import forms

from .models import Recipe


class RecipeForm(forms.ModelForm):
    image = forms.ImageField(
        required=True,
        label='Изображение',
        error_messages={'required': 'Пожалуйста, загрузите изображение'}
        )

    class Meta:
        model = Recipe
        fields = ('title', 'image', 'tag', 'time', 'ingredients',
                  'description')
