from celery import shared_task
from django.utils import timezone
from .models import User

@shared_task
def update_user_status():
    avlusers = User.objects.filter(status='AVL', assigned_till__lt=timezone.now())
    avlusers.update(status='WRK', assigned_till=None)

    astusers = User.objects.filter(status='AST', assigned_till__lt=timezone.now())
    astusers.update(status='WRK', assigned_till=None, assigned_to=None)