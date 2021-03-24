from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from api.models import Favorites, Shoplist

User = get_user_model()


class CreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("first_name", "username", "email")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            Favorites.objects.create(user=user)
            Shoplist.objects.create(user=user)
        return user
