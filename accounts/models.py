from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

from .utils import generate_random_color
# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    ROLE_CHOICES = [
        ('PM', 'Project Manager'),
        ('PC', 'Project Coordinator'),
        ('HR', 'HR Manager'),
        ('SA', 'System Admin'),
        ('AC', 'Accountant'),
        ('OE', 'Office Executive'),
        ('GD', 'Graphic Designer'),
        ('FD', 'Frontend Developer'),
        ('BD', 'Backend Developer'),
    ]
    username = None
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, null=True)
    local_address = models.CharField(max_length=200, null=True)
    native_address = models.CharField(max_length=200, null=True)
    date_of_birth = models.DateField(null=True)
    reporting_manager = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
    role = models.CharField(max_length=5, choices=ROLE_CHOICES, default='OE')
    designation = models.CharField(max_length=150, null=True)
    profile_color = models.CharField(max_length=10, default=generate_random_color())

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def get_first_letter(self):
        return self.first_name[:1]
    
    def __str__(self):
        return self.email