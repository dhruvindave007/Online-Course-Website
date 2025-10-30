from django import forms
from django.contrib.auth import get_user_model
User = get_user_model()

from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    contact = forms.CharField(max_length=10, min_length=10, required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)


    class Meta:
        model = User
        fields = ['username', 'email', 'contact', 'first_name', 'last_name']