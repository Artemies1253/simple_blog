from django import forms
from .models import Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=20, label=_("Имя"))
    last_name = forms.CharField(max_length=20, label=_("Фамилия"))
    phone = forms.CharField(max_length=20, required=False, label=_("Телефон"))
    city = forms.CharField(max_length=40, required=False, label=_("Город"))

    class Meta:
        model = User
        fields = ["username", "password1", "password2",
                  "first_name", "last_name", "phone", "city"]


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=20, required=False, label=_("Имя"))
    last_name = forms.CharField(max_length=20, required=False, label=_("Фамилия"))

    class Meta:
        model = Profile
        fields = ["first_name", "last_name", "phone", "city"]
