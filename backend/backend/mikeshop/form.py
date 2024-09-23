from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.forms import ModelForm, ModelChoiceField
from django.db import transaction

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_admin = False
        user.save()
        return user