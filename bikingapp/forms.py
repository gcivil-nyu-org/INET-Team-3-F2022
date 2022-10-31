from django import forms
from django.forms import (
    TextInput,
    DateTimeInput,
    RadioSelect,
    Select,
    Textarea,
)
from .models import Event
from .widgets import DatePickerInput, TimePickerInput


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = (
            "title",
            "location",
            "borough",
            "state",
            "zipcode",
            "date",
            "time",
            "date_created",
            "event_type",
            "description",
            "created_by",
        )
        widgets = {
            "title": TextInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 92%; margin-bottom: 10px;display: inline-block;",  # noqa: E501
                    "placeholder": "Title",
                }
            ),
            "location": TextInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 88%; margin-bottom: 10px;display: inline-block;",  # noqa: E501
                }
            ),
            "borough": Select(
                attrs={
                    "class": "btn dropdown-toggle",
                    "style": "max-width: 35%; display: inline-block; border: 1px solid lightgray;",  # noqa: E501
                }
            ),
            "state": TextInput(
                attrs={
                    "class": "form-control",
                    "readonly": "readonly",
                    "style": "max-width: 19%;margin-bottom: 10px; display: inline-block;",  # noqa: E501
                }
            ),
            "zipcode": TextInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 20%; margin-bottom: 10px; display: inline-block;",  # noqa: E501
                    "placeholder": "Zip",
                }
            ),
            "date": DatePickerInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 30%; margin-bottom: 10px;display: inline-block;",  # noqa: E501
                }
            ),
            "time": TimePickerInput(
                attrs={
                    "step": "any",
                    "class": "form-control",
                    "style": "max-width: 30%; margin-bottom: 10px;display: inline-block;",  # noqa: E501
                }
            ),
            "date_created": DateTimeInput(
                attrs={
                    "readonly": "readonly",
                    "class": "form-control",
                    "style": "max-width: 58%; margin-bottom: 10px;display: inline-block;",  # noqa: E501
                }
            ),
            "event_type": RadioSelect(
                attrs={
                    "class": "custom-radio-list",
                    "style": "max-width: 300px; margin-bottom: 10px;",
                }
            ),
            "description": Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "style": "max-width: 100%; margin-bottom: 10px;",
                }
            ),
            "created_by": TextInput(
                attrs={
                    "class": "form-control",
                    "readonly": "readonly",
                    "style": "max-width: 65%; display: inline-block;",
                }
            ),
        }
