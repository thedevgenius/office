from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView

from .forms import SigninForm
# Create your views here.

class SigninView(LoginView):
    template_name = 'accounts/sign_in.html'
    redirect_authenticated_user = True
    form_class = SigninForm

class DashboardView(TemplateView):
    template_name = 'accounts/dashboard.html'


class UserAddView(TemplateView):
    template_name = 'accounts/user_add.html'