from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

User = get_user_model()

# TODO шифрование пароля в форме, сделать на основе UserCreationForm?
#  Почитать про неё подробно, про её кастомизацию, там наверное есть
#  шифрование пароля
class CreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "username", "email", 'password')

    def clean_password(self):
        password = self.cleaned_data.get('password')
        password_validation.validate_password(password)

        return password

