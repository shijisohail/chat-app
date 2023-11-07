# user_management/forms.py

from django import forms
from .models import User


class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "phone_number", 'username', 'email', 'password')

