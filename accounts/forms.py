from django import forms
from django.contrib.auth.forms import AuthenticationForm

class SigninForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'class':'input', 'placeholder':'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}))