from django import forms
from django.contrib.auth.models import User, Permission

class UserForm(forms.Form):
    username = forms.CharField(max_length=100)
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField()
