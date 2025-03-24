from datetime import datetime, time, timedelta
from django import forms
from django.utils import timezone
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


from .models import User

class SigninForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'class':'input', 'placeholder':'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}))


class UserAddForm(forms.ModelForm):
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
    first_name = forms.CharField(required=True, widget=forms.TextInput())
    last_name = forms.CharField(required=True, widget=forms.TextInput())
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    reporting_manager = forms.ModelChoiceField(required=False, queryset=User.objects.filter(role='PM'))
    role = forms.CharField(widget=forms.Select(choices=ROLE_CHOICES))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'date_of_birth', 'reporting_manager', 'role', 'designation']

    def __init__(self, *args, **kwargs):
        super(UserAddForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'role' or field_name == 'reporting_manager':
                field.widget.attrs['class'] = 'select'
            else:
                field.widget.attrs['class'] = 'input'


class TeamBookForm(forms.Form):
    id = forms.IntegerField(widget=forms.HiddenInput())
    # hour = forms.ChoiceField(choices=[])
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        now = timezone.localtime()
        

        hour_options = [(i, i) for i in range(now.hour, 20)]
        self.fields['hour'] = forms.ChoiceField(choices=hour_options, label='Hour', widget=forms.Select(attrs={'class':'select'}))

        minute_options = [(i, f"{i:02d}") for i in range(0, 60)]
        self.fields['minute'] = forms.ChoiceField(choices=minute_options, label='Minute', widget=forms.Select(attrs={'class':'select'}))
    
class AssistForm(TeamBookForm):
    manager = forms.ModelChoiceField(queryset=User.actives.filter(role='PM'), widget=forms.Select(attrs={'class':'select'}))
