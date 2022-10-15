from django import forms
from django.forms import ModelForm, TextInput, EmailInput, DateTimeInput
from .models import Event
'''
class EventForm(forms.Form):
    location = forms.CharField(required=False)
    date_time = forms.DateTimeField(label='Event Date/Time',required=False)
    public_private = forms.ChoiceField(choices=[('public','Public'),('private','Private')])
    description = forms.CharField(widget = forms.Textarea,required=False)
'''

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('location','date_time', 'date_created', 'public_private','description','created_by')
        widgets = {
            'location': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px; margin-bottom: 10px;',
                'placeholder': 'Address'
                }),
            'date_time': DateTimeInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 300px; margin-bottom: 10px;'
                }),
            'date_created': DateTimeInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 300px; margin-bottom: 10px;'
                }),
            'public_private': TextInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 300px; margin-bottom: 10px;'
                }),
            'description': TextInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 300px; margin-bottom: 10px;'
                }),
            'created_by': TextInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 300px;'
                })
        }
