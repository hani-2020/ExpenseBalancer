from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    def clean_username(self):
        username = self.cleaned_data.get("username")
        return username

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')