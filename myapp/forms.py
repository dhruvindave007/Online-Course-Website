from django import forms
from django.contrib.auth import get_user_model
from .models import Category, SuggestedCourse

User = get_user_model()

from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    contact = forms.CharField(max_length=10, min_length=10, required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)

    class Meta:
        model = User
        fields = ["username", "email", "contact", "first_name", "last_name"]


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "slug"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "slug": forms.TextInput(attrs={"class": "form-control"}),
        }


class SuggestedCourseForm(forms.ModelForm):
    class Meta:
        model = SuggestedCourse
        fields = ["course", "order"]
        widgets = {
            "course": forms.Select(attrs={"class": "form-control"}),
            "order": forms.NumberInput(attrs={"class": "form-control"}),
        }
