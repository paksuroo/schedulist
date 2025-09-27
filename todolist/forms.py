from django import forms
from django.utils import timezone
from .models import Event

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=20)
    password = forms.CharField(label='Password', max_length=20)

class AddTaskForm(forms.Form):
    task_name = forms.CharField(label='Task Name', max_length=50)
    description = forms.CharField(label='Description', max_length=200)

class UpdateTaskForm(forms.Form):
    task_name = forms.CharField(label='Task Name', max_length=50)
    description = forms.CharField(label='Description', max_length=200)
    status = forms.CharField(label='Status', max_length=50)

class RegisterForm(forms.Form):
    username = forms.CharField(label='Username', max_length=50)
    first_name = forms.CharField(label='First Name', max_length=50)
    last_name = forms.CharField(label='Last Name', max_length=50)
    email = forms.CharField(label='Email', max_length=50)
    password = forms.CharField(label='Password', max_length=50)
    confirm_password = forms.CharField(label='Confirm Password', max_length=50)

class AddEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['event_name', 'description', 'event_date', 'status']  # include status
        widgets = {
            'event_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter event name',
                'maxlength': '50'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe your event...'
            }),
            'event_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'id': 'eventDatePicker',
                'placeholder': 'Select date and time'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control',
            }),
        }

    def clean_event_date(self):
        event_date = self.cleaned_data['event_date']
        if event_date < timezone.now():
            raise forms.ValidationError("Event date cannot be in the past.")
        return event_date