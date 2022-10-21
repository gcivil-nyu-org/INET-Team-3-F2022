from django       import forms
from django.forms import TextInput, DateTimeInput, TimeInput, DateInput, RadioSelect, SelectDateWidget
from .models      import Event

class EventForm(forms.ModelForm):
    class Meta:
        model   = Event
        fields  = ('location','date', 'time', 'date_created', 'public_private','description','created_by')
        widgets = {
            'location': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px; margin-bottom: 10px;',
                'placeholder': 'Address'
                }),
            'date': SelectDateWidget(attrs={
                'class': "form-control", 
                'style': 'max-width: 300px; margin-bottom: 10px;'
                }),
            'time': TimeInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 300px; margin-bottom: 10px;'
                }),
            'date_created': DateTimeInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 300px; margin-bottom: 10px;',
                }),
            'public_private': RadioSelect(attrs={
                'class': "custom-radio-list", 
                #'style': 'max-width: 300px; margin-bottom: 10px;'
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
