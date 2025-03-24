from datetime import datetime, time, timedelta
from django import forms
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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        now = datetime.now().time()
        
        start_hour = max(now.hour, 9)
        start_minute = max((now.minute // 15 + 1) * 15, 60) if now.hour >= 9 else 60

        if start_minute == 60:
            start_time = time(start_hour + 1, 0)
        else:
            start_time = time(start_hour, start_minute)

        end_time = time(19, 15)

        time_options = []
        current_time = start_time
        while current_time <= end_time:
            time_options.append((current_time.strftime('%H:%M'), current_time.strftime('%H:%M')))
            current_time = (datetime.combine(datetime.today(), current_time) + timedelta(minutes=15)).time()  # Increment by 15 minutes

        # Add the time options to the form field
        self.fields['time'] = forms.ChoiceField(choices=time_options)
    
class AssistForm(TeamBookForm):
    manager = forms.ModelChoiceField(queryset=User.actives.filter(role='PM'), widget=forms.Select(attrs={'class':'select'}))
