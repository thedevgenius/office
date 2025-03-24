from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

from .utils import generate_random_color
from .managers import ActiveUserManager, EmployeeManager
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
    STATUS_CHOICE = [
        ('WRK', 'Working'),
        ('BKD', 'Booked'),
        ('AVL', 'Available'),
        ('AST', 'Assist'),
        ('ABS', 'Absent')
    ]
    username = None
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, null=True)
    local_address = models.CharField(max_length=200, null=True, blank=True)
    native_address = models.CharField(max_length=200, null=True, blank=True)
    date_of_birth = models.DateField(null=True)
    reporting_manager = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='teams')
    role = models.CharField(max_length=5, choices=ROLE_CHOICES, default='OE')
    designation = models.CharField(max_length=150, null=True)
    profile_color = models.CharField(max_length=10, default=generate_random_color())

    assigned_to = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    is_pool = models.BooleanField(default=False, null=True, blank=True)
    status = models.CharField(max_length=5, choices=STATUS_CHOICE, default='WRK')
    assigned_till = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    actives = ActiveUserManager()
    employees = EmployeeManager()

    def get_first_letter(self):
        return self.first_name[:1]
    
    def get_status(self):
        return dict(self.STATUS_CHOICE)[self.status]
    
    def get_status_class(self):
        if self.status == 'WRK':
            return 'primary'
        elif self.status == 'BKD':
            return 'info'
        elif self.status == 'AVL':
            return 'success'
        elif self.status == 'AST':
            return 'warning'
        elif self.status == 'ABS':
            return 'danger'
        
    
    def __str__(self):
        return f'{self.get_full_name()} - {self.designation}'
    
    # def save(self, *args, **kwargs):
    #     self.set_password(self.password)
    #     return super().save(*args, **kwargs)