from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import SigninView, DashboardView, UserAddView, EmployeeListView, BookView, FreeView, AssistView

urlpatterns = [
    path('', SigninView.as_view(), name='login'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('employee/add/', UserAddView.as_view(), name='employee_add'),
    path('employee/list/', EmployeeListView.as_view(), name='employee_list'),

    path('get-book/', BookView.as_view(), name='book'),
    path('free/', FreeView.as_view(), name='free'),
    path('assist/', AssistView.as_view(), name='assist'),
]
