from django.db import models

class ActiveUserManager(models.Manager):
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_active=True).order_by('first_name')
        return queryset

class EmployeeManager(models.Manager):
    roles = ['GD', 'FD', 'BD']
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_active=True, role__in=self.roles).order_by('first_name')
        return queryset