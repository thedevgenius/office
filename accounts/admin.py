from django.contrib import admin
from .models import User
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'designation', 'reporting_manager']

admin.site.register(User, UserAdmin)

