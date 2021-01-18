from django.forms import ModelMultipleChoiceField, ModelForm, \
    CheckboxSelectMultiple

from .models import Recipe, TimeTag

class RecipeForm(ModelForm):

    # TODO сейчас соединяется с объектом таймтега, но как сделать так,
    #  чтобы соединялось с полями объекта таймтега?
    # tag = ModelMultipleChoiceField(queryset=TimeTag.objects.all())
    class Meta:
        model = Recipe
        fields = ('title', 'ingredients', 'image', 'tag', 'cooking_time',
                  'description')

    # def __init__(self, *args, **kwargs):
    #     super(RecipeForm, self).__init__(*args, **kwargs)
    #
    #     self.fields['tag'].widget = CheckboxSelectMultiple(
    #         choices=self.fields['tag'].choices)