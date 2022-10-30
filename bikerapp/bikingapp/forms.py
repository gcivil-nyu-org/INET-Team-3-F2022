from django       import forms
from django.forms import TextInput, DateTimeInput, TimeInput, DateInput, RadioSelect, SelectDateWidget
from .models      import Event
from .widgets import DatePickerInput, TimePickerInput, DateTimePickerInput
#NSWER_CHOICES = [("public","Public"),("public","Private")]
class EventForm(forms.ModelForm):
    # event_type = forms.ChoiceField(
    #     required=True,
    #     widget=forms.RadioSelect,
    #     choices=ANSWER_CHOICES,
    # )
    class Meta:
        model   = Event
        fields  = ('title','location','state','zipcode','date', 'time', 'date_created', 'event_type','description','created_by')
        widgets = {
            'title': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 90%; margin-bottom: 10px;display: inline-block;',
                'placeholder': 'Title'
                }),
            'location': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 83%; margin-bottom: 10px;display: inline-block;',
                }),
            'state': TextInput(attrs={
                'class': "form-control", 
                'readonly':'readonly',
                'style': 'max-width: 30%; display: inline-block;'
                }),
            'zipcode':TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 30%; margin-bottom: 10px; display: inline-block;',
                'placeholder': 'Zipcode'
                }),
            'date': DatePickerInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 50%; margin-bottom: 10px;display: inline-block;',
                }),
            'time': TimePickerInput(attrs={
                'step':"any",
                'class': "form-control", 
                'style': 'max-width: 50%; margin-bottom: 10px;display: inline-block;'
                }),
            'date_created': DateTimeInput(attrs={
                'readonly':'readonly',
                'class': "form-control", 
                'style': 'max-width: 45%; margin-bottom: 10px;display: inline-block;',
                }),
            'event_type': RadioSelect(attrs={
                'class': "custom-radio-list", 
                'style': 'max-width: 300px; margin-bottom: 10px;'
                }),
            'description': TextInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 100%; margin-bottom: 10px;'
                }),
            'created_by': TextInput(attrs={
                'class': "form-control", 
                'readonly':'readonly',
                'style': 'max-width: 50%; display: inline-block;'
                })
        }
