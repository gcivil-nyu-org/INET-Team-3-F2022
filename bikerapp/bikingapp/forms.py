from django import forms
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
        fields = ('location','date_time','date_created','public_private','description','created_by')
