from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import SigninView, DashboardView, UserAddView

urlpatterns = [
    path('', SigninView.as_view(), name='login'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('user/add/', UserAddView.as_view(), name='user_add'),
]
